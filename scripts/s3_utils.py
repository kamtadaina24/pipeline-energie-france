from botocore.exceptions import ClientError
import boto3
import os

BUCKET = "raw"


def get_s3_client():
    """Les valeurs par defaut visent le S3 local ; sur AWS on definit les variables."""
    return boto3.client(
        "s3",
        endpoint_url=os.getenv("S3_ENDPOINT", "http://localhost:8333"),
        aws_access_key_id=os.getenv("S3_ACCESS_KEY", "minioadmin"),
        aws_secret_access_key=os.getenv("S3_SECRET_KEY", "minioadmin123"),
        region_name="us-east-1",
    )

def ensure_bucket(s3):
    try:
        s3.create_bucket(Bucket=BUCKET)
    except ClientError as e:
        if e.response["Error"]["Code"] not in ("BucketAlreadyOwnedByYou", "BucketAlreadyExists"):
            raise
