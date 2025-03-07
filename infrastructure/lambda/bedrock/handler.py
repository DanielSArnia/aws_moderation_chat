import json
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a Bedrock client
bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")  # Adjust the region if needed

# Lambda handler function
def lambda_handler(event, context):
    """
    Lambda function to interact with AWS Bedrock. The event should contain input data for the model.
    """

    # Log the incoming event
    logger.info(f"Received event: {json.dumps(event)}")

    # Example: Extract input data from event (adjust based on your specific needs)
    try:
        input_data = event.get("body")
        if not input_data:
            raise ValueError("No input data provided in the event body")

        # If input_data is a string, convert it to a JSON object
        if isinstance(input_data, str):
            input_data = json.loads(input_data)
        
        # Here, input_data should contain the model-specific data to send to Bedrock
        prompt = input_data.get("prompt", "Default prompt")  # Example of prompt extraction

        # Calling bedrock's text generation model
        response = bedrock_client.invoke_model(
            modelId="bedrock-text-generation-model",
            body=json.dumps({"prompt": prompt}),
            contentType="application/json",
            accept="application/json"
        )

        # Process the response from Bedrock
        response_body = json.loads(response["body"].read().decode("utf-8"))
        generated_text = response_body.get("generatedText", "No text generated.")

        # Log the generated text
        logger.info(f"Generated text: {generated_text}")

        # Return the response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Successfully generated text from Bedrock model",
                "generatedText": generated_text
            })
        }
    
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            })
        }
