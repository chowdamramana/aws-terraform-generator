from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def help_page(request: Request):
    resources = [
        {"name": "Terraform AWS Provider", "url": "https://registry.terraform.io/providers/hashicorp/aws/latest/docs"},
        {"name": "Terraform Documentation", "url": "https://www.terraform.io/docs"},
        {"name": "AWS Modules", "url": "https://github.com/terraform-aws-modules"}
    ]
    return templates.TemplateResponse(
        "help.html",
        {"request": request, "resources": resources}
    )