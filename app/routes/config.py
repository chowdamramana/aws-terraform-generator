from fastapi import APIRouter, Depends, HTTPException
from app.models.config import AWSConfig
from app.services.database import save_config, get_user_configs
from app.models.user import User
from fastapi_users import FastAPIUsers
from app.routes.auth import fastapi_users, auth_backend

router = APIRouter(prefix="/config", tags=["config"])

@router.post("/", response_model=dict)
async def create_config(config: AWSConfig, current_user: User = Depends(fastapi_users.current_user())):
    try:
        config_id = save_config(config, current_user.id)
        return {"config_id": config_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[AWSConfig])
async def list_configs(current_user: User = Depends(fastapi_users.current_user())):
    try:
        configs = get_user_configs(current_user.id)
        return configs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))