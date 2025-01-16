#src/config/aws_s3.py
import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def upload_to_s3(file, bucket_name, object_name):
    """
    Uploads a file to an S3 bucket and returns the file's public URL.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials are not set correctly in environment variables.")
    
    s3 = boto3.client(
        "s3", 
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=region
    )

    try:
        s3.upload_fileobj(file, bucket_name, object_name)
        image_url = f"https://{bucket_name}.s3.{region}.amazonaws.com/{object_name}"
        return image_url
    except (NoCredentialsError, PartialCredentialsError):
        raise ValueError("Invalid AWS credentials.")
    except Exception as e:
        raise ValueError(f"Failed to upload file to S3: {e}")
