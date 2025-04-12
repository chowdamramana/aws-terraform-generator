from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.user import User
from app.services.database import get_user_configs
from app.routes.auth import fastapi_users

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, user: User = Depends(fastapi_users.current_user())):
    configs = get_user_configs(user.id)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "configs": configs, "user": user}
    )