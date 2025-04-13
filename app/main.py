import sys
import os
print("Current working directory:", os.getcwd())
print("Python sys.path:", sys.path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://frontend"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Setup authentication (optional)
setup_auth(app)

# Include routers
app.include_router(config_router, prefix="/config", tags=["config"])
app.include_router(home_router, tags=["home"])

@app.on_event("startup")
async def startup_event():
    logger = structlog.get_logger()
    logger.info("Application startup")