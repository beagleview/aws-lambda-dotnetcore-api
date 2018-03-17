import json
import logging
import os
import time
import uuid
import datetime

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
    stStatus =  data['status']
    item = {
            'id': str(uuid.uuid1()),
            'fname': data['fname'],
            'lname': data['lname'],
            'nickname': data['nickname'],
            'gender': data['gender'],
            'room': data['room'],
            'no': data['no'],
            'status': stStatus,
            'checked': False,
            'createdAt': timestamp,
            'updatedAt': timestamp,
        }

    if stStatus == '1':
        item.update({
            'university ':data['university'],
            'major':data['major']
        })
        

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
