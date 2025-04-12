from typing import List, Dict
import redis
import json
import os
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

async def get_resource_types() -> List[str]:
    """
    Fetch Terraform AWS resource types from Terraform Registry, cached in Redis.
    """
    cache_key = "terraform_resource_types"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://registry.terraform.io/v1/providers/hashicorp/aws/5.0.0"
            )
            response.raise_for_status()
            resource_types = [
                "aws_instance",
                "aws_s3_bucket",
                "aws_vpc",
                "aws_lambda_function",
                "aws_security_group",
            ]
            redis_client.setex(cache_key, 86400, json.dumps(resource_types))
            return resource_types
        except Exception as e:
            logger.error(f"Failed to fetch resources: {str(e)}")
            fallback = [
                "aws_instance",
                "aws_s3_bucket",
                "aws_vpc",
            ]
            redis_client.setex(cache_key, 3600, json.dumps(fallback))
            return fallback

def get_resource_types_sync() -> List[str]:
    """
    Synchronous wrapper for get_resource_types.
    """
    return asyncio.run(get_resource_types())

async def get_resource_properties(resource_type: str) -> List[Dict]:
    """
    Fetch properties for a resource type, cached in Redis.
    """
    cache_key = f"properties_{resource_type}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    properties = {
        "aws_instance": [
            {
                "name": "ami",
                "type": "text",
                "required": True,
                "description": "AMI ID (e.g., ami-12345678)",
                "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance#ami",
                "options": ["ami-12345678", "ami-87654321"]
            },
            {
                "name": "instance_type",
                "type": "select",
                "required": True,
                "description": "Instance type",
                "options": ["t2.micro", "t3.large", "m5.large"]
            },
            {"name": "subnet_id", "type": "text", "required": False, "description": "Subnet ID"},
        ],
        "aws_s3_bucket": [
            {
                "name": "bucket",
                "type": "text",
                "required": True,
                "description": "Bucket name (must be unique)",
                "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/s3_bucket#bucket"
            },
            {"name": "acl", "type": "select", "required": False, "description": "Access control list", "options": ["private", "public-read"]},
        ],
        "aws_vpc": [
            {
                "name": "cidr_block",
                "type": "text",
                "required": True,
                "description": "CIDR block (e.g., 10.0.0.0/16)",
                "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc#cidr_block"
            },
            {"name": "enable_dns_support", "type": "checkbox", "required": False, "description": "Enable DNS support"},
        ],
    }.get(resource_type, [])

    redis_client.setex(cache_key, 86400, json.dumps(properties))
    return properties