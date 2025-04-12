from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import Base
from app.models.config import AWSConfig, ResourceConfig
import os
import json
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_size=10 if os.getenv("ENVIRONMENT") == "prod" else 5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Database init failed: {str(e)}")
        raise

def save_config(config: AWSConfig, user_id: int) -> int:
    with SessionLocal() as db:
        try:
            db_config = {
                "user_id": user_id,
                "name": config.name,
                "region": config.region,
                "resources": json.dumps([r.dict() for r in config.resources]),
                "version": config.version
            }
            db.execute(
                """
                INSERT INTO configs (user_id, name, region, resources, version)
                VALUES (:user_id, :name, :region, :resources, :version)
                """,
                db_config
            )
            db.commit()
            result = db.execute("SELECT LAST_INSERT_ID()").scalar()
            logger.info(f"Saved config ID {result} for user {user_id}")
            return result
        except Exception as e:
            logger.error(f"Failed to save config: {str(e)}")
            db.rollback()
            raise

def get_user_configs(user_id: int) -> List[AWSConfig]:
    with SessionLocal() as db:
        try:
            result = db.execute(
                "SELECT id, name, region, resources, version FROM configs WHERE user_id = :user_id",
                {"user_id": user_id}
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
                        version=row.version
                    )
                )
            return configs
        except Exception as e:
            logger.error(f"Failed to fetch configs: {str(e)}")
            raise