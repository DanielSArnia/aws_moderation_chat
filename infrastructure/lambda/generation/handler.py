import json
import os
import boto3
from copy import deepcopy
from decimal import Decimal

from prompts import (
    system_string,
    input_template,
    system_string_batch_verification,
    input_template_batch_verification,
    tool_list_generate,
    tool_list_validate,
)

# define bedrock client and model id
bedrock_client = boto3.client("bedrock-runtime", region_name="eu-west-1")
# model_id = "eu.anthropic.claude-3-5-sonnet-20240620-v1:0"  # Use a specific model ID from Bedrock
model_id = "eu.anthropic.claude-3-haiku-20240307-v1:0"  # Use a specific model ID from Bedrock

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
generated_nickname_table_name = os.environ.get("GENERATED_NICKNAME_TABLE")
generated_nickname_table = dynamodb.Table(generated_nickname_table_name)
nickname_table_name = os.environ.get("NICKNAME_TABLE")
nickname_table = dynamodb.Table(nickname_table_name)


def handler(event, context):
    try:
        # Extract nickname from event body (API Gateway sends this in 'body')
        if "body" in event:
            body = json.loads(event["body"])
        else:
            body = event  # fallback for direct Lambda testing

        age_range = body.get("age_range", "")
        lego_themes = body.get("lego_themes", "")
        interests = body.get("interests", "")
        region_code = body.get("region_code", "")

        # Create prompt for the model
        formatted_system_string = "".join(system_string)
        input_string = "".join(input_template)
        formatted_input_string = input_string.format(
            age_range=age_range,
            interests=interests,
            lego_themes=lego_themes,
            region_code=region_code,
        )

        llm_response = make_bedrock_llm_call(
            system_string=formatted_system_string,
            prompt_string=formatted_input_string,
            tool_name="generate_nicknames",
            tools=tool_list_generate,
            temperature=0.7,
            max_tokens=4096,
        )

        nicknames = llm_response["nicknames"]
        filtered_nicknames = []

        for nickname in nicknames:
            # check name availability
            response = nickname_table.get_item(Key={"nickname": nickname["nickname"]})

            if "Item" in response:
                # Nickname already exists
                print(f"Nickname '{nickname['nickname']}' already exists in the table.")
            else:
                filtered_nicknames.append(nickname)

        if len(filtered_nicknames) < 0:
            return build_api_response(
                400, json.dumps({"error": f"No new nicknames could be generated."})
            )

        # Create prompt for the model batch verification
        formatted_system_string_verification = "".join(system_string_batch_verification)
        input_string_verification = "".join(input_template_batch_verification)
        formatted_input_string_verification = input_string_verification.format(
            nicknames=str(filtered_nicknames),
            age_range=age_range,
            region_code=region_code,
        )

        llm_response = make_bedrock_llm_call(
            system_string=formatted_system_string_verification,
            prompt_string=formatted_input_string_verification,
            tools=tool_list_validate,
            tool_name="validate_nicknames",
            max_tokens=4096,
        )

        validated_nicknames = llm_response["validation_results"]
        filtered_nicknames = [
            gn for gn in validated_nicknames if gn["passes_validation"] == True
        ]

        all_data_nicknames = merge_nickname_dicts(nicknames, validated_nicknames)

        save_to_dynamodb(
            interests=interests,
            lego_themes=lego_themes,
            age_range=age_range,
            region_code=region_code,
            nicknames=all_data_nicknames,
        )

        return build_api_response(200, json.dumps({"result": all_data_nicknames}))
    except Exception as e:
        print(f"Failed to generate response: {str(e)}")
        return build_api_response(500, json.dumps({"error": str(e)}))


def make_bedrock_llm_call(
    system_string,
    prompt_string,
    tools,
    tool_name,
    temperature: float = 0.2,
    max_tokens: int = 500,
):
    # Prepare Claude-specific request payload (Anthropic format)
    messages = [{
        "role": "user",
        "content": [
            {"text": system_string},
            {"text": f"<instructions>\n{prompt_string}\n</instructions>\n"},
        ],
    }]

    retries = 0
    while retries < 5:
        try:
            # Call Bedrock runtime for inference
            response = bedrock_client.converse(
                modelId=model_id,
                messages=messages,
                inferenceConfig={
                    "maxTokens": max_tokens,
                    "temperature": temperature,
                },
                toolConfig={
                    "tools": tools,
                    "toolChoice": {"tool": {"name": tool_name}},
                },
                # accept="application/json",
                # contentType="application/json"
            )

            # Read the response stream and get the tool output
            response_message = response["output"]["message"]
            response_content_blocks = response_message["content"]
            content_block = next(
                (block for block in response_content_blocks if "toolUse" in block), None
            )
            tool_use_block = content_block["toolUse"]
            tool_result_dict = tool_use_block["input"]

            return tool_result_dict

        except Exception as e:
            print(f"Model failed to generate response:: {str(e)}")
            retries += 1
            if retries == 5:
                raise e
    raise


def save_to_dynamodb(lego_themes, interests, age_range, region_code, nicknames):
    """
    Save the nickname details and the LLM response to DynamoDB.
    """
    try:
        for original_nickname in nicknames:
            nickname = deepcopy(original_nickname)
            item = {
                "nickname": nickname["nickname"],  # Unique ID for each record
                "age_range": age_range,
                "lego_themes": lego_themes,
                "interests": interests,
                "region_code": region_code,
                "metadata": convert_numbers_to_decimal(nickname),
            }

            generated_nickname_table.put_item(Item=item)
            print(f"Saved item to DynamoDB: {item}")

    except Exception as e:
        print(f"Failed to save to DynamoDB: {str(e)}")
        raise e


def convert_numbers_to_decimal(obj):
    if isinstance(obj, dict):
        return {k: convert_numbers_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numbers_to_decimal(elem) for elem in obj]
    elif isinstance(obj, float):
        return Decimal(str(obj))  # Convert float to Decimal
    else:
        return obj


def build_api_response(code, json_body):
    return {
        "statusCode": code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Optional for CORS
        },
        "body": json_body,
    }


def merge_nickname_dicts(nicknames, validated_nicknames):
    # Build a lookup dictionary for validated nicknames (assuming uniqueness on 'nickname')
    validated_lookup = {vn['nickname']: vn for vn in validated_nicknames}

    # Merge dictionaries where nicknames match
    all_data_nicknames = [
        {**nickname, **validated_lookup[nickname['nickname']]}
        for nickname in nicknames
        if nickname['nickname'] in validated_lookup
    ]
    return all_data_nicknames