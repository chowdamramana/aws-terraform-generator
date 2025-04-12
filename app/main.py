from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes.auth import setup_auth
from app.routes.config import router as config_router
from app.routes.home import router as home_router
from app.services.database import init_db
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)

app = FastAPI(
    title="AWS Terraform Generator",
    description="Generate Terraform code for AWS resources",
    version="1.0.0",
)

# Initialize database
init_db()

# Setup authentication
setup_auth(app)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")

# Include routers
app.include_router(config_router)
app.include_router(home_router)