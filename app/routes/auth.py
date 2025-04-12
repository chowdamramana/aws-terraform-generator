from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from app.models.user import User, UserDB
from app.services.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
import os

SECRET = os.getenv("SECRET_KEY", "your-secret-key")

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

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

def setup_auth(app: FastAPI):
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
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