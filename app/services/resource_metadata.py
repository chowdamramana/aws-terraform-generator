from typing import List, Dict
import redis
import json
import os
import httpx
import structlog

logger = structlog.get_logger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

async def get_resource_types() -> List[str]:
    """
    Fetch Terraform AWS resource types from Terraform Registry, cached in Redis.
    """
    cache_key = "terraform_resource_types"
    cached = redis_client.get(cache_key)
    if cached:
        logger.info("Resource types cache hit")
        return json.loads(cached)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://registry.terraform.io/v1/providers/hashicorp/aws/latest"
            )
            response.raise_for_status()
            # Parse resource types (mocked for now, extend with real parsing)
            resource_types = [
                "aws_instance",
                "aws_s3_bucket",
                "aws_vpc",
                "aws_lambda_function",
                "aws_security_group",
                "aws_rds_instance",
                "aws_elb",
            ]  # TODO: Parse from API schema
            redis_client.setex(cache_key, 86400, json.dumps(resource_types))
            logger.info("Fetched resource types", count=len(resource_types))
            return resource_types
        except Exception as e:
            logger.error("Failed to fetch resources", error=str(e))
            fallback = [
                "aws_instance",
                "aws_s3_bucket",
                "aws_vpc",
            ]
            redis_client.setex(cache_key, 3600, json.dumps(fallback))
            return fallback

async def get_resource_properties(resource_type: str) -> List[Dict]:
    """
    Fetch properties for a resource type, cached in Redis.
    """
    cache_key = f"properties_{resource_type}"
    cached = redis_client.get(cache_key)
    if cached:
        logger.info("Properties cache hit", resource_type=resource_type)
        return json.loads(cached)

    # Static for simplicity; extend with API parsing
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
        "aws_lambda_function": [
            {
                "name": "function_name",
                "type": "text",
                "required": True,
                "description": "Unique name for Lambda function",
                "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function#function_name"
            },
            {
                "name": "runtime",
                "type": "select",
                "required": True,
                "description": "Runtime environment",
                "options": ["nodejs20.x", "python3.12", "java21"]
            },
        ],
        "aws_security_group": [
            {
                "name": "name",
                "type": "text",
                "required": True,
                "description": "Security group name",
                "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group#name"
            },
            {
                "name": "vpc_id",
                "type": "text",
                "required": False,
                "description": "VPC ID"
            },
        ],
        "aws_rds_instance": [
            {
                "name": "instance_class",
                "type": "select",
                "required": True,
                "description": "Instance class",
                "options": ["db.t3.micro", "db.m5.large"],
                "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/rds#instance_class"
            },
            {
                "name": "engine",
                "type": "select",
                "required": True,
                "description": "Database engine",
                "options": ["mysql", "postgres"]
            },
        ],
        "aws_elb": [
            {
                "name": "name",
                "type": "text",
                "required": True,
                "description": "Load balancer name",
                "doc_url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/elb#name"
            },
            {
                "name": "subnets",
                "type": "text",
                "required": True,
                "description": "List of subnet IDs"
            },
        ],
    }.get(resource_type, [])

    redis_client.setex(cache_key, 86400, json.dumps(properties))
    logger.info("Fetched properties", resource_type=resource_type, count=len(properties))
    return properties