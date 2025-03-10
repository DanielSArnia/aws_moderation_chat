import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CONNECTION_TABLE')
connections_table = dynamodb.Table(table_name)

def handler(event, context):
    connection_id = event['requestContext']['connectionId']
    print(f"Connect event: {connection_id}")

    # Store connection ID in DynamoDB
    connections_table.put_item(Item={'connectionId': connection_id})

    return {
        'statusCode': 200,
        'body': 'Connected.'
    }