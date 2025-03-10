import boto3
import os
import json
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CONNECTION_TABLE')
connections_table = dynamodb.Table(table_name)

def handler(event, context):
    print("Received event:", json.dumps(event))

    connection_id = event['requestContext']['connectionId']
    route_key = event['requestContext']['routeKey']

    # The WebSocket API endpoint (for sending messages)
    domain_name = event['requestContext']['domainName']
    stage = event['requestContext']['stage']
    endpoint_url = f"https://{domain_name}/{stage}"

    apigw_management_api = boto3.client('apigatewaymanagementapi',
        endpoint_url=endpoint_url
    )

    if route_key == 'sendMessage':
        body = json.loads(event['body'])
        message = body.get('message', 'No message provided')

        print(f"Broadcasting message: {message} from {connection_id}")

        # Fetch all active connections from DynamoDB
        try:
            response = connections_table.scan(ProjectionExpression='connectionId')
            items = response.get('Items', [])

            for item in items:
                target_connection_id = item['connectionId']
                try:
                    # Send the message to each connected client
                    apigw_management_api.post_to_connection(
                        ConnectionId=target_connection_id,
                        Data=json.dumps({
                            'from': connection_id,
                            'message': message
                        }).encode('utf-8')
                    )
                except ClientError as e:
                    if e.response['Error']['Code'] == 'GoneException':
                        print(f"Stale connection {target_connection_id}, deleting...")
                        connections_table.delete_item(Key={'connectionId': target_connection_id})
                    else:
                        print(f"Error sending message to {target_connection_id}: {str(e)}")

        except Exception as e:
            print(f"Error fetching connection IDs: {str(e)}")

    return {
        'statusCode': 200,
        'body': 'Message processed'
    }
