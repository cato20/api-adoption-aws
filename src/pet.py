import json
import boto3
import os


animal_adoption_table= os.environ['ADOPTION_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(animal_adoption_table)

def getPets(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    
    path = event["path"]
    array_path = path.split("/")
    user_id =array_path[-1]
    print(user_id)
    return {
        'statusCode': 200,
        'body': json.dumps("Hello from get Lambda")
    }
    
def updatePet(event, context):
    print(json.dumps({"running": True}))
    print(json.dumps(event))
    path = event["path"]
    array_path = path.split("/")
    user_id =array_path[-1]
    body = event["body"]
    print(body)
    # bodyObject = json.loads(body)
    # table.put_item(
    #     Item={
    #         'pk': user_id,
    #         'sk': 'age',
    #         'name': bodyObject['name'],
    #         'last_name': bodyObject['last_name'],
    #         'age': bodyObject['age']
    #     }
    # )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
