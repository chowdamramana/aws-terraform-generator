import redis
import json
import os
from typing import List, Dict
import structlog
from tenacity import retry, stop_after_attempt, wait_fixed

logger = structlog.get_logger(__name__)

redis_client = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"))

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_cached_data(key: str) -> List[Dict]:
    try:
        cached = redis_client.get(key)
        return json.loads(cached) if cached else None
    except Exception as e:
        logger.error(f"Redis get failed: {str(e)}")
        return None

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def cache_data(key: str, data: List[Dict], ttl: int = 86400):
    try:
        redis_client.setex(key, ttl, json.dumps(data))
        logger.info(f"Cached data: {key}")
    except Exception as e:
        logger.error(f"Redis set failed: {str(e)}")