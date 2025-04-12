from fastapi import APIRouter, Depends, HTTPException
from app.models.config import AWSConfig, TerraformOutput
from app.services.database import save_config, get_user_configs
from app.services.terraform_generator import generate_terraform_code
from app.models.user import User
from app.routes.auth import fastapi_users
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/config", tags=["config"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=dict)
@limiter.limit("5/minute")
async def create_config(config: AWSConfig, current_user: User = Depends(fastapi_users.current_user())):
    try:
        config_id = save_config(config, current_user.id)
        return {"config_id": config_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[AWSConfig])
async def list_configs(current_user: User = Depends(fastapi_users.current_user())):
    try:
        configs = get_user_configs(current_user.id)
        return configs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{config_id}/terraform", response_model=TerraformOutput)
async def generate_terraform(config_id: int, current_user: User = Depends(fastapi_users.current_user())):
    try:
        configs = get_user_configs(current_user.id)
        config = next((c for c in configs if c.id == config_id), None)
        if not config:
            raise HTTPException(status_code=404, detail="Config not found")
        return generate_terraform_code(config)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))