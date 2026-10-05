"""AWS SDK client for S3 and SageMaker operations."""

from typing import Optional

import boto3
from botocore.exceptions import ClientError


def create_s3_client(region: str = "us-east-1"):
    """Create boto3 S3 client."""
    return boto3.client("s3", region_name=region)


def create_sagemaker_client(region: str = "us-east-1"):
    """Create boto3 SageMaker client."""
    return boto3.client("sagemaker", region_name=region)


def upload_to_s3(
    client,
    bucket: str,
    key: str,
    body: bytes,
    content_type: str = "application/octet-stream",
) -> bool:
    """Upload object to S3 bucket."""
    try:
        client.put_object(Bucket=bucket, Key=key, Body=body, ContentType=content_type)
        return True
    except ClientError:
        return False


def list_sagemaker_endpoints(client) -> list:
    """List SageMaker inference endpoints."""
    response = client.list_endpoints()
    return response.get("Endpoints", [])
