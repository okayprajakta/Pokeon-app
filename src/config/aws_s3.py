import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from fastapi import HTTPException, UploadFile
import imghdr

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

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "tiff", "gif", "bmp", "raw"}
ALLOWED_MIME_TYPES = {"image/jpg","image/jpeg", "image/png", "image/tiff", "image/gif", "image/bmp", "image/x-raw"}

def validate_image_file(file: UploadFile):
    # Check file extension
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file extension provided. Allowed extensions: jpg, jpeg, png, tiff, gif, bmp, raw")

    # Check MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type provided. Allowed MIME types: image/jpeg, image/png, image/tiff, image/gif, image/bmp, image/x-raw")

    # Check if the file is a valid image
    file.file.seek(0)
    if imghdr.what(file.file) not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid image file")
    file.file.seek(0)


def check_image_exists_in_s3(bucket_name: str, object_name: str) -> bool:
    """Check if an image exists in the S3 bucket."""
    s3 = boto3.client('s3')
    try:
        s3.head_object(Bucket=bucket_name, Key=object_name)
        return True
    except ClientError:
        return False