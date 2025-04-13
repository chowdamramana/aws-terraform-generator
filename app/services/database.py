from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models.user import Base
from app.models.config import AWSConfig, ResourceConfig
import os
import json
import structlog
from typing import List
from tenacity import retry, stop_after_attempt, wait_fixed

logger = structlog.get_logger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_size=10 if os.getenv("ENVIRONMENT") == "prod" else 5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized")
    except Exception as e:
        logger.error("Database init failed", error=str(e))
        raise

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def save_config(config: AWSConfig, user_id: int) -> int:
    with SessionLocal() as db:
        try:
            db_config = {
                "user_id": user_id,
                "name": config.name,
                "region": config.region,
                "resources": json.dumps([r.dict() for r in config.resources]),
                "version": config.version,
            }
            result = db.execute(
                text(
                    """
                    INSERT INTO configs (user_id, name, region, resources, version)
                    VALUES (:user_id, :name, :region, :resources, :version)
                    """
                ),
                db_config,
            )
            db.commit()
            config_id = db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
            logger.info("Saved config", config_id=config_id, user_id=user_id)
            return config_id
        except Exception as e:
            logger.error("Failed to save config", error=str(e))
            db.rollback()
            raise

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def get_user_configs(user_id: int) -> List[AWSConfig]:
    with SessionLocal() as db:
        try:
            result = db.execute(
                text(
                    "SELECT id, name, region, resources, version FROM configs WHERE user_id = :user_id"
                ),
                {"user_id": user_id},
            ).fetchall()
            configs = []
            for row in result:
                resources = [ResourceConfig(**r) for r in json.loads(row.resources)]
                configs.append(
                    AWSConfig(
                        id=row.id,
                        user_id=user_id,
                        name=row.name,
                        region=row.region,
                        resources=resources,
                        version=row.version,
                    )
                )
            logger.info("Fetched configs", user_id=user_id, count=len(configs))
            return configs
        except Exception as e:
            logger.error("Failed to fetch configs", error=str(e))
            raise