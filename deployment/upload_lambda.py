import os
import json
import uuid
import boto3
from botocore.config import Config

s3_client = boto3.client(
    's3',
    region_name=os.environ.get('AWS_REGION', 'eu-north-1'),
    config=Config(signature_version='s3v4')
)

BUCKET_NAME = "s3-upload-bucket-firewatch" 

def generate_url(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename', 'data.csv')
        file_id = str(uuid.uuid4())
        s3_key = f"{file_id}/{filename}"
        presigned_url = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': s3_key,
                'ContentType': "text/csv"
            },
            ExpiresIn=900
        )
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "uploadUrl": presigned_url,
                "fileId": file_id,
                "s3Key": s3_key
            })
        }
    except Exception as e:
        return{
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


