from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import aiofiles

router = APIRouter(tags=["home"])

@router.get("/", response_class=HTMLResponse)
async def home():
    async with aiofiles.open("frontend/dist/index.html", mode="r") as f:
        return await f.read()