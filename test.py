import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def upload_file_to_s3(file_name: str, bucket_name: str, object_name: str = None):

    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f"File '{file_name}' successfully uploaded to bucket '{bucket_name}' as '{object_name}'.")
        return True
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        return False
    except NoCredentialsError:
        print("Error: No AWS credentials found.")
        return False
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


if __name__ == "__main__":

    file_name = "Notes.txt"
    bucket_name = "pokemon-s3-apro64"  
    object_name = "notes.txt" 

    uploaded = upload_file_to_s3(file_name, bucket_name, object_name)
    if uploaded:
        print("Upload completed successfully.")
    else:
        print("Upload failed.")
