import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CONNECTION_TABLE')
connections_table = dynamodb.Table(table_name)

def handler(event, context):
    connection_id = event['requestContext']['connectionId']
    print(f"Disconnect event: {connection_id}")

    # Remove connection ID from DynamoDB
    connections_table.delete_item(Key={'connectionId': connection_id})

    return {
        'statusCode': 200,
        'body': 'Disconnected.'
    }