import uuid
from datetime import datetime

from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


class User:
    def __init__(
        self,
        id: str,
        email: str,
        hashed_password: str,
        name: str | None = None,
        created_at: datetime | None = None,
    ):
        self.id = id
        self.email = email
        self.hashed_password = hashed_password
        self.name = name
        self.created_at = created_at or datetime.utcnow()


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def hash_password(self, password: str) -> str:
        return get_password_hash(password)

    async def get_by_email(self, email: str) -> User | None:
        # Placeholder - actual implementation would query database
        return None

    async def get_by_id(self, user_id: str) -> User | None:
        # Placeholder - actual implementation would query database
        return None

    async def create(self, email: str, hashed_password: str, name: str | None = None) -> User:
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            hashed_password=hashed_password,
            name=name,
            created_at=datetime.utcnow(),
        )
        # Placeholder - actual implementation would save to database
        return user
