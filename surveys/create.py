import json
import logging
import os
import time
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')
def create(event, context):
    data = json.loads(event['body'])
    if 'fname' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'fname': data['fname'],
        'lname': data['lname'],
        'nickname': data['nickname'],
        'gender': data['gender'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
