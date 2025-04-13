from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from app.models.user import User, UserDB
from app.services.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
import os
from datetime import timedelta
from fastapi.responses import JSONResponse

SECRET = os.environ.get("SECRET_KEY") or ValueError("SECRET_KEY not set")

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600, refresh_lifetime_seconds=86400)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

async def get_user_db():
    async with AsyncSession(engine) as session:
        yield SQLAlchemyUserDatabase(session, UserDB)

fastapi_users = FastAPIUsers[User, int](
    get_user_db,
    [auth_backend],
)

router = fastapi_users.get_auth_router(auth_backend)

@router.post("/jwt/refresh")
async def refresh_token(user: User = Depends(fastapi_users.current_user(active=True))):
    token = await fastapi_users.auth_backend.get_strategy().write_token(user)
    return JSONResponse({"access_token": token, "token_type": "bearer"})

def setup_auth(app: FastAPI):
    app.include_router(
        router,
        prefix="/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(User, User),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(User, User),
        prefix="/users",
        tags=["users"],
    )