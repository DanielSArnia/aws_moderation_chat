import json
import boto3

def handler(event, context):
    # Create a Bedrock runtime client
    bedrock_client = boto3.client('bedrock-runtime', region_name="eu-west-1")

    # Claude 3 Sonnet model ID (you can replace it with another one)
    # model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"  # Use a specific model ID from Bedrock
    model_id = "eu.anthropic.claude-3-5-sonnet-20240620-v1:0"  # Use a specific model ID from Bedrock

    # Extract nickname from event body (API Gateway usually sends this in 'body')
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event  # fallback for direct Lambda testing

    nickname = body.get('nickname', '')
    age_range = body.get('age_range', '')
    region_code = body.get('region_code', '')


    system_string = (
        "You are evaluating a child's nickname for the LEGO platform.\n",
        "Your task is to analyze this nickname against corporate guidelines, safety policies, and regulations.\n"
        "Provide a structured JSON response with detailed scores and explanations."
    )

    # Create prompt for the model
    input_template = (
        "Evaluate the following nickname:\n",
        "\n",
        "Nickname: \"{nickname}\"\n",
        "Platform: LEGO Kids Community\n",
        "User Age Range: {age_range}\n",
        "Region: {region_code}\n",
        "\n",
        "Provide a detailed analysis covering:\n",
        "1. Inappropriate Content: Detect profanity, adult themes, violence, bullying, drugs, or other inappropriate content (even in coded language or slang)\n",
        "2. Personal Information: Identify potential PII including names, locations, ages, schools, or anything that could identify a child\n",
        "3. Brand Alignment: Assess if the nickname aligns with LEGO's positive, creative, family-friendly brand values\n",
        "4. Age Appropriateness: Determine if the nickname is suitable for all users in a children's platform\n",
        "5. Regional Compliance: Check for region-specific concerns relating to COPPA, GDPR, or other relevant regulations\n",
        "\n",
        "Return your analysis in the following JSON format:\n",
        "{{\n",
        "  \"analysis\": {{\n",
        "    \"inappropriate_content\": {{\n",
        "      \"score\": <0-1 value, lower is better>,\n",
        "      \"pass\": <boolean>,\n",
        "      \"explanation\": <string>\n",
        "    }},\n",
        "    \"personal_information\": {{\n",
        "      \"score\": <0-1 value, lower is better>,\n",
        "      \"pass\": <boolean>,\n",
        "      \"explanation\": <string>\n",
        "    }},\n",
        "    \"brand_alignment\": {{\n",
        "      \"score\": <0-1 value, higher is better>,\n",
        "      \"pass\": <boolean>,\n",
        "      \"explanation\": <string>\n",
        "    }},\n",
        "    \"age_appropriate\": {{\n",
        "      \"score\": <0-1 value, higher is better>,\n",
        "      \"pass\": <boolean>,\n",
        "      \"explanation\": <string>\n",
        "    }},\n",
        "    \"regional_compliance\": {{\n",
        "      \"pass\": <boolean>,\n",
        "      \"explanation\": <string>\n",
        "    }}\n",
        "  }},\n",
        "  \"overall_result\": {{\n",
        "    \"valid\": <boolean>,\n",
        "    \"confidence\": <0-1 value>,\n",
        "    \"decision_explanation\": <string>,\n",
        "    \"risk_level\": <\"none\"|\"low\"|\"medium\"|\"high\">\n",
        "  }}\n",
        "}}\n"
    )
    
    input_string = "".join(input_template)
    formatted_input_string = input_string.format(
        nickname=nickname,
        age_range=age_range,
        region_code=region_code
    )

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
                        "text": formatted_input_string
                    }
                ]
            }
        ],
        "max_tokens": 500,
        "temperature": 0.2,
        "anthropic_version": "bedrock-2023-05-31"  # Required for Claude v3
    }

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
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # Optional for CORS
            },
            "body": json.dumps({
                "result": completion
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }