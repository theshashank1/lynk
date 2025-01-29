import os

import boto3
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def get_aws_session():
    """
    Create a boto3 session using AWS credentials stored in environment variables.
    """
    return boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME"),
    )


def get_aws_client(session: boto3.Session, service_name: str):
    """
    Create a boto3 client for a specific AWS service using the provided session.

    :param session: A boto3 Session object.
    :param service_name: The name of the AWS service to create a client for.
    :return: A boto3 Client object.
    """
    return session.client(service_name)


if __name__ == "__main__":

    # Get a session
    session = get_aws_session()

    # Get a client for S3
    s3_client = get_aws_client(session, "s3")

    # Execute an S3 command
    response = s3_client.list_buckets()
    print("S3 Buckets:", response["Buckets"])
