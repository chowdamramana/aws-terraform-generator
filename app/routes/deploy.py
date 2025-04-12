from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def deploy(request: Request):
    steps = [
        "Install Terraform: `brew install terraform` or download from terraform.io",
        "Initialize: `terraform init`",
        "Plan: `terraform plan`",
        "Apply: `terraform apply`"
    ]
    return templates.TemplateResponse(
        "deploy.html",
        {"request": request, "steps": steps}
    )