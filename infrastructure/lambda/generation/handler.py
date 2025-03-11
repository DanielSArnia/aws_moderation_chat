import json
import os
import boto3
from copy import deepcopy
from decimal import Decimal

from prompts import system_string, input_template, system_string_batch_verification, input_template_batch_verification

# define bedrock client and model id
bedrock_client = boto3.client('bedrock-runtime', region_name="eu-west-1")
model_id = "eu.anthropic.claude-3-5-sonnet-20240620-v1:0"  # Use a specific model ID from Bedrock

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
generated_nickname_table_name = os.environ.get("GENERATED_NICKNAME_TABLE")
generated_nickname_table = dynamodb.Table(generated_nickname_table_name)
nickname_table_name = os.environ.get("NICKNAME_TABLE")
nickname_table = dynamodb.Table(nickname_table_name)

def handler(event, context):
    try:
        # Extract nickname from event body (API Gateway sends this in 'body')
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event  # fallback for direct Lambda testing

        age_range = body.get('age_range', '')
        lego_themes = body.get('lego_themes', '')
        interests = body.get('interests', '')
        region_code = body.get('region_code', '')


        # Create prompt for the model
        formatted_system_string = "".join(system_string)
        input_string = "".join(input_template)
        formatted_input_string = input_string.format(
            age_range=age_range,
            interests=interests,
            lego_themes=lego_themes,
            region_code=region_code
        )

        llm_response = make_bedrock_llm_call(
            system_string=formatted_system_string,
            prompt_string=formatted_input_string,
            temperature=0.7
        )

        nicknames = llm_response['nicknames']
        filtered_nicknames = []

        for nickname in nicknames:
            # check name availability
            response = nickname_table.get_item(Key={'nickname': nickname['nickname']})

            if 'Item' in response:
                # Nickname already exists
                print(f"Nickname '{nickname['nickname']}' already exists in the table.")
            else:
                filtered_nicknames.append(nickname)
        
        if len(filtered_nicknames) < 0:
            return build_api_response(
                400,
                json.dumps({
                    "error": f"No new nicknames could be generated."
                })
            )
        

        # Create prompt for the model batch verification
        formatted_system_string_verification = "".join(system_string_batch_verification)
        input_string_verification = "".join(input_template_batch_verification)
        formatted_input_string_verification = input_string_verification.format(
            nicknames=str(filtered_nicknames),
            age_range=age_range,
            region_code=region_code
        )

        llm_response = make_bedrock_llm_call(
            system_string=formatted_system_string_verification,
            prompt_string=formatted_input_string_verification,
        )

        generated_nicknames = llm_response['validation_results']
        filtered_nicknames = [gn for gn in generated_nicknames if gn['passes_validation'] == True]

        save_to_dynamodb(
            interests=interests,
            lego_themes=lego_themes,
            age_range=age_range,
            region_code=region_code,
            nicknames=generated_nicknames
        )

        return build_api_response(
            200,  
            json.dumps({
                "result": filtered_nicknames
            })
        )
    except Exception as e:
        print(f"Failed to generate response: {str(e)}")
        return build_api_response(
            500,
            json.dumps({
                "error": str(e)
            })
        )

def make_bedrock_llm_call(system_string, prompt_string, temperature:float=0.2, max_tokens:int=500, anthropic_version:str="bedrock-2023-05-31"):
    # Prepare Claude-specific request payload (Anthropic format)
    body_payload = {
        "messages": [
            {
                "role": "system",
                "content": [{
                    "type": "text",
                    "text": system_string
                }],
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt_string
                    }
                ]
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "anthropic_version": anthropic_version  # Required for Claude v3
    }

    retries = 0
    while retries < 5:
        try:
            # Call Bedrock runtime for inference
            response = bedrock_client.invoke_model(
                modelId=model_id,
                body=json.dumps(body_payload),
                accept="application/json",
                contentType="application/json"
            )

            # Read the response stream and decode it
            response_body = json.loads(response['body'].read())

            # Claude models return `completion` in the result
            completion = response_body['content'][0]['text']

            # Return the response as HTTP response (if triggered via API Gateway)
            return json.loads(completion)

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
                'nickname': nickname['nickname'],  # Unique ID for each record
                'age_range': age_range,
                'lego_themes': lego_themes,
                'interests': interests,
                'region_code': region_code,
                'metadata': convert_numbers_to_decimal(nickname)
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
            "Access-Control-Allow-Origin": "*"  # Optional for CORS
        },
        "body": json_body
    }
