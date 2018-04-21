import json
import logging
import os
import time
import uuid
import datetime
import boto3

dynamodb = boto3.resource('dynamodb')
def create(event, context):
    data = event
    if 'fname' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the todo item.")
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    try :
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
                'createdAt': timestamp,
                'updatedAt': timestamp,
            }

        if stStatus == '1':
            project = ''
            try:
                project = data['projectname']
            finally:
                project = ''
            item.update({
                'university':data['university'],
                'faculty':data['faculty'],
                'major':data['major'],
                'round':data['round'],
                'confirm':data['confirm'],
                'project': project
            })
        elif stStatus =='2' :
            item.update({
                'university':data['uni'],
                'faculty':data['fac'],
                'major':data['maj']
            })
        elif stStatus == '5':
            item.update({
                'condition':data['condition']
            })
            
        # write the todo to the database
        table.put_item(Item=item)

        # create a response
        response = {
            "statusCode": 200,
            "body": json.dumps(item)
        }
    except ValueError:
        response = {
            "statusCode": 504,
            "body": json.dumps(item)
        }
    except:
        response = {
            "statusCode": 500,
            "body": json.dumps(item)
        }

    return response
