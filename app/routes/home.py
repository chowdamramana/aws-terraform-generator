from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["home"])

@router.get("/", response_class=HTMLResponse)
async def home():
    return "<html><body>Redirecting to frontend...</body></html>"