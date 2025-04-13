from github import Github
from typing import List, Dict
from app.services.cache import get_cached_data, cache_data
import structlog
from tenacity import retry, stop_after_attempt, wait_fixed

logger = structlog.get_logger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_aws_modules() -> List[Dict]:
    cache_key = "terraform_modules"
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    g = Github()  # Unauthenticated access
    try:
        repos = g.search_repositories(query="org:terraform-aws-modules")
        modules = []
        for repo in repos[:5]:  # Limit to top 5 to avoid rate limits
            try:
                release = repo.get_latest_release()
                modules.append(
                    {
                        "name": repo.name.replace("terraform-aws-", ""),
                        "version": release.tag_name if release else "latest",
                        "url": repo.html_url,
                        "description": repo.description or "",
                    }
                )
            except:
                continue
        if not modules:
            raise Exception("No modules found")
        cache_data(cache_key, modules, ttl=604800)  # Cache for 7 days
        return modules
    except Exception as e:
        logger.error(f"Failed to fetch modules: {str(e)}")
        # Fallback to static list to avoid breaking UI
        fallback = [
            {
                "name": "vpc",
                "version": "latest",
                "url": "https://github.com/terraform-aws-modules/terraform-aws-vpc",
                "description": "VPC module for AWS",
            },
            {
                "name": "s3-bucket",
                "version": "latest",
                "url": "https://github.com/terraform-aws-modules/terraform-aws-s3-bucket",
                "description": "S3 bucket module for AWS",
            },
        ]
        cache_data(cache_key, fallback, ttl=3600)  # Cache fallback for 1 hour
        return fallback