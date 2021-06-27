import json
import boto3
import base64
import os
import uuid

animal_adoption_table= os.environ['ADOPTION_TABLE']

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(animal_adoption_table)
s3 = boto3.client('s3')
bucketName = 'bucket-pets'
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

def uploadImages(arrayPictures):
    for picture in arrayPictures:
        name = str(uuid.uuid1()) +".png"
        decodeImg = base64.b64decode(picture)
        s3.put_object(Bucket=bucketName,Key=name,Body=decodeImg)
        location = s3.get_bucket_location(Bucket=bucketName)['LocationConstraint']
        objectUrl = "https://%s.s3-%s.amazonaws.com/%s" % (bucketName,location, name)
        print("This is the url in s3:",objectUrl)
def updateInfo(pk,sk,health,age,location):
    response = table.update_item(
        Key={
            'pk':pk,
            'sk':sk
        },
        UpdateExpression="set age=:a,healt_status=:h,location=:l",
        ExpressionAttributeValues={
            ':a':Numeric(age),
            ':h':health,
            ':l':location
        }
        ReturnValues="Update_New"
    )
    
def updatePet(event, context):
    path = event["path"]
    array_path = path.split("/")
    pet_id =array_path[-1]
    body = event["body"]
    bodyObject = json.loads(body)
    print(bodyObject)
     
    if bodyObject["pictures"]:
        uploadImages(bodyObject["pictures"])
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
