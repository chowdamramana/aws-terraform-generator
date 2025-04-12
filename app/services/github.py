from github import Github
from typing import List, Dict
from app.services.cache import get_cached_modules, cache_modules
import logging

logger = logging.getLogger(__name__)

def fetch_aws_modules() -> List[Dict]:
    """
    Fetch Terraform AWS modules without authentication, cached in Redis.
    """
    cached = get_cached_modules()
    if cached:
        return cached

    g = Github()
    try:
        repo = g.get_repo("terraform-aws-modules/terraform-aws-vpc")
        modules = [
            {
                "name": "vpc",
                "version": repo.get_latest_release().tag_name,
                "url": repo.html_url,
                "description": "VPC module for AWS"
            },
            # Add other modules
        ]
        cache_modules(modules)
        return modules
    except Exception as e:
        logger.error(f"Failed to fetch modules: {str(e)}")
        return [{"name": "error", "description": "Failed to fetch modules"}]