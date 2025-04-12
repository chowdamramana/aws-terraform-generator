from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.session import SessionMiddleware
from app.routes import auth, config, dashboard, deploy, help, home, modules, preview
from app.services.database import init_db
import os

app = FastAPI(title="AWS Terraform Generator")

# Initialize database
init_db()

# Setup authentication
auth.setup_auth(app)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Session middleware for preview
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "your-secret-key"))

# Include routers
app.include_router(config.router)
app.include_router(dashboard.router)
app.include_router(deploy.router)
app.include_router(help.router)
app.include_router(home.router)
app.include_router(modules.router)
app.include_router(preview.router)