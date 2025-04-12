from fastapi import APIRouter
from app.services.resource_metadata import get_resource_types, get_resource_properties
from typing import List, Dict

router = APIRouter(prefix="/api", tags=["resources"])

@router.get("/resource-types", response_model=List[str])
async def list_resource_types():
    return await get_resource_types()

@router.get("/properties/{resource_type}", response_model=List[Dict])
async def list_properties(resource_type: str):
    return await get_resource_properties(resource_type)