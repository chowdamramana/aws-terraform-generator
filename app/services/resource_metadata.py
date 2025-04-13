from typing import List, Dict
import redis
import json
import os
import httpx
import structlog
import subprocess
import tempfile
from tenacity import retry, stop_after_attempt, wait_fixed

logger = structlog.get_logger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_resource_types() -> List[str]:
    cache_key = "terraform_resource_types"
    cached = redis_client.get(cache_key)
    if cached:
        logger.info("Resource types cache hit")
        return json.loads(cached)

    try:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            subprocess.run(
                ["terraform", "providers", "schema", "-json"],
                stdout=tmp,
                check=True,
            )
            with open(tmp.name, "r") as f:
                schema = json.load(f)
        resource_types = list(
            schema.get("provider_schemas", {})
            .get("registry.terraform.io/hashicorp/aws", {})
            .get("resource_schemas", {})
            .keys()
        )
        redis_client.setex(cache_key, 86400, json.dumps(resource_types))
        logger.info("Fetched resource types", count=len(resource_types))
        return resource_types
    except Exception as e:
        logger.error("Failed to fetch resources", error=str(e))
        fallback = ["aws_instance", "aws_s3_bucket", "aws_vpc"]
        redis_client.setex(cache_key, 3600, json.dumps(fallback))
        return fallback

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_resource_properties(resource_type: str) -> List[Dict]:
    cache_key = f"properties_{resource_type}"
    cached = redis_client.get(cache_key)
    if cached:
        logger.info("Properties cache hit", resource_type=resource_type)
        return json.loads(cached)

    try:
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            subprocess.run(
                ["terraform", "providers", "schema", "-json"],
                stdout=tmp,
                check=True,
            )
            with open(tmp.name, "r") as f:
                schema = json.load(f)
        properties = (
            schema.get("provider_schemas", {})
            .get("registry.terraform.io/hashicorp/aws", {})
            .get("resource_schemas", {})
            .get(resource_type, {})
            .get("block", {})
            .get("attributes", {})
        )
        result = [
            {
                "name": name,
                "type": prop.get("type", "string"),
                "required": prop.get("required", False),
                "description": prop.get("description", ""),
                "options": prop.get("enum", []) if prop.get("type") == "string" else [],
            }
            for name, prop in properties.items()
        ]
        redis_client.setex(cache_key, 86400, json.dumps(result))
        logger.info("Fetched properties", resource_type=resource_type, count=len(result))
        return result
    except Exception as e:
        logger.error("Failed to fetch properties", error=str(e))
        return []