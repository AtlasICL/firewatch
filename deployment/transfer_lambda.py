import json
import os
import uuid
from typing import Any

import boto3
from botocore.config import Config

s3_client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION", "eu-north-1"),
    config=Config(signature_version="s3v4"),
)
# Fixed upload bucket name.
BUCKET_NAME = "s3-upload-bucket-firewatch"
"""
Lambda function for getting presigned URLs for download and upload
for firewatch csvs.

Args:
    `event`: Dictonary containing passed data from HTTP request.
    `context`: Context object for lambda runtime, unused.
Returns:
    HTTP reply indicating success, containing relevant presigned URLs.
"""


def generate_url(event: dict[str, Any], context: Any) -> dict[str, Any]:
    try:
        # Retrieve event dictionary, instantiate related variables.
        body: dict[str, Any] = json.loads(event.get("body", "{}"))
        filename: str = body.get("filename", "data.csv")
        file_id: str = str(uuid.uuid4())  # UUID for uploaded files.
        input_s3_key: str = (
            f"{file_id}/{filename}"  # S3 key for location of file.
        )
        # Generate upload url based on s3_key.
        presigned_upload_url: str = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": input_s3_key,
                "ContentType": "text/csv",
            },
            ExpiresIn=900,
        )
        # Return URL.
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {
                    "upload_url": presigned_upload_url,
                    "file_id": file_id,
                    "input_s3_key": input_s3_key,
                }
            ),
        }
    # Return error message.
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
