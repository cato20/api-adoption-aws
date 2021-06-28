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
    uris=[]
    for picture in arrayPictures:
        name = str(uuid.uuid1()) +".png"
        decodeImg = base64.b64decode(picture)
        s3.put_object(Bucket=bucketName,Key=name,Body=decodeImg)
        location = s3.get_bucket_location(Bucket=bucketName)['LocationConstraint']
        objectUrl = "https://%s.s3-%s.amazonaws.com/%s" % (bucketName,location, name)
        uris.append(objectUrl)
        print("This is the url in s3:",objectUrl)
    return uris
    
def updateInfo(pk,sk,health,age,locationUpdate,uris):
    response = table.update_item(
        Key={
            'pk':pk,
            'sk':sk
        },
        UpdateExpression="set age=:a,health_status=:h,#location=:l,pictures=:p",
        ExpressionAttributeValues={
            ':a': age,
            ':h': health,
            ':l': locationUpdate,
            ':p': uris
        },
        ExpressionAttributeNames={
            '#location':'l'
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
def updatePet(event, context):
    message=""
    path = event["path"]
    array_path = path.split("/")
    sk=event["queryStringParameters"]["type"]
    pet_id =array_path[-1]
    bodyObject = json.loads(event["body"])
    health_status = bodyObject["health_status"]
    age = bodyObject["age"]
    location = bodyObject["location"]

    if bodyObject["pictures"]:
        updateUris = uploadImages(bodyObject["pictures"])
        message=updateInfo(str(pet_id),sk,health_status,age,location,updateUris)
    return {
        'statusCode': 200,
        'body': json.dumps("updated movie succeded")
    }
