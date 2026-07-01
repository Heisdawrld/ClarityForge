from fastapi import APIRouter

from api.v1.endpoints import auth, health, reasoning, sessions

router = APIRouter()

router.include_router(health.router, tags=["health"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(reasoning.router, prefix="/reasoning", tags=["reasoning"])
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
