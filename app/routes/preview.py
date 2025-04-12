from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from app.services.terraform import generate_terraform_files
from app.models.config import AWSConfig
import zipfile
import os
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def preview(request: Request):
    config_data = request.session.get("config")
    if not config_data:
        return templates.TemplateResponse(
            "error.html",
            {"request": request, "message": "No configuration found"}
        )
    config = AWSConfig(**json.loads(config_data))
    files = generate_terraform_files(config)
    return templates.TemplateResponse(
        "preview.html",
        {"request": request, "terraform_code": files.get("main.tf", "")}
    )

@router.get("/download")
async def download_terraform(request: Request):
    config_data = request.session.get("config")
    if not config_data:
        return {"error": "No configuration found"}
    
    config = AWSConfig(**json.loads(config_data))
    files = generate_terraform_files(config)
    
    os.makedirs("temp", exist_ok=True)
    for filename, content in files.items():
        with open(f"temp/{filename}", "w") as f:
            f.write(content)
    
    zip_path = "temp/terraform.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for filename in files.keys():
            z.write(f"temp/{filename}", filename)
    
    return FileResponse(
        zip_path,
        filename="terraform_config.zip",
        media_type="application/zip"
    )