from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.github import fetch_aws_modules

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def modules(request: Request):
    modules = fetch_aws_modules()
    return templates.TemplateResponse(
        "modules.html",
        {"request": request, "modules": modules}
    )