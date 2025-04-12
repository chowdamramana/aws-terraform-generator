import redis
import json
import os
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

def get_cached_modules() -> List[Dict]:
    try:
        cached = redis_client.get("terraform_modules")
        return json.loads(cached) if cached else None
    except Exception as e:
        logger.error(f"Redis get failed: {str(e)}")
        return None

def cache_modules(modules: List[Dict]):
    try:
        redis_client.setex("terraform_modules", 86400, json.dumps(modules))
        logger.info("Cached Terraform modules")
    except Exception as e:
        logger.error(f"Redis set failed: {str(e)}")