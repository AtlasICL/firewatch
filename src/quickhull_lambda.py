import csv
import json
import os
from pathlib import Path
from typing import Any

import boto3
from botocore.config import Config

from src.parser import Parser
from src.point import HullInput, Point
from src.quickhull import quickhull

BUCKET_NAME: str = "s3-upload-bucket-firewatch"

s3_client = boto3.client(
    "s3",
    region_name=os.environ.get("AWS_REGION", "eu-north-1"),
    config=Config(signature_version="s3v4"),
)


def lambda_handler(event: dict[str, Any], context: Any):
    try:
        body: dict[str, Any] = json.loads(event.get("body", "{}"))
        input_s3_key: str = body.get("input_s3_key", "premade_files/data.csv")
        s3_path = Path(input_s3_key)
        output_s3_key: str = f"{s3_path.parent}/{s3_path.stem}_quickhull.csv"
        local_csv_path: Path = Path("/tmp/current.csv")

        s3_client.download_file(
            Bucket=BUCKET_NAME, Key=input_s3_key, Filename=str(local_csv_path)
        )

        # Quickhull calls
        input_points: tuple[Point, ...] = Parser.parse(local_csv_path)
        quickhull_input: HullInput = HullInput(input_points)
        convex_hull: list[Point] = quickhull(quickhull_input)

        with local_csv_path.open(
            mode="w", encoding="utf-8", newline=""
        ) as csvfile:
            writer = csv.writer(csvfile)
            for point in convex_hull:
                writer.writerow([point.x, point.y])
                print(f"x = {point.x}  |  y = {point.y}")

        s3_client.upload_file(
            Bucket=BUCKET_NAME,
            Key=output_s3_key,
            Filename=str(local_csv_path),
        )

        # Generate download url based on s3_key.
        presigned_download_url: str = s3_client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": BUCKET_NAME, "Key": output_s3_key},
            ExpiresIn=900,
        )
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {
                    "output_key": output_s3_key,
                    "download_url": presigned_download_url,
                }
            ),
        }
    except Exception as e:
        print(f"Download Failed: {e}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
    finally:
        local_csv_path.unlink(missing_ok=True)
