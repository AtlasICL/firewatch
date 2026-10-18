import json
import os
import uuid
from typing import Any

import boto3
from botocore.config import Config

BUCKET_NAME: str = "s3-upload-bucket-firewatch"

s3_client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION", "eu-north-1"),
    config=Config(signature_version="s3v4"),
)


def generate_url(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """
    Lambda function for getting a presigned upload URL for firewatch
    csvs.

    Args:
        `event`: Dictionary containing passed data from HTTP request.
        `context`: Context object for lambda runtime, unused.
    Returns:
        HTTP reply indicating success, containing the presigned upload
        URL, the file ID, and the S3 key the file will be stored at.
    """

    try:
        # Retrieve event dictionary, instantiate related variables.
        body: dict[str, Any] = json.loads(event.get("body", "{}"))
        filename: str = body.get("filename", "data.csv")
        uploaded_file_uuid: str = str(uuid.uuid4())
        input_s3_key: str = (
            f"{uploaded_file_uuid}/{filename}"  # S3 key for location of file.
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

        # Return upload URL, file ID, and S3 key.
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {
                    "upload_url": presigned_upload_url,
                    "file_id": uploaded_file_uuid,
                    "input_s3_key": input_s3_key,
                }
            ),
        }
    # Return error message.
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
