from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select

from api.v1.endpoints.auth import get_current_user
from db.database import get_db

router = APIRouter()


class SessionCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., description="The reasoning session content")


class SessionUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None


class SessionResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: str
    updated_at: str


class SessionListResponse(BaseModel):
    sessions: list[SessionResponse]
    total: int
    page: int
    page_size: int


@router.get("/", response_model=SessionListResponse)
async def list_sessions(
    current_user: Annotated[dict, Depends(get_current_user)],
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    db=Depends(get_db),
):
    # Placeholder - actual implementation would query database
    return SessionListResponse(
        sessions=[],
        total=0,
        page=page,
        page_size=page_size,
    )


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db=Depends(get_db),
):
    # Placeholder - actual implementation would query database
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Session not found",
    )


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session: SessionCreate,
    current_user: Annotated[dict, Depends(get_current_user)],
    db=Depends(get_db),
):
    # Placeholder - actual implementation would create in database
    return SessionResponse(
        id="placeholder-id",
        title=session.title,
        content=session.content,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z",
    )


@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    updates: SessionUpdate,
    current_user: Annotated[dict, Depends(get_current_user)],
    db=Depends(get_db),
):
    # Placeholder - actual implementation would update in database
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Session not found",
    )


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db=Depends(get_db),
):
    # Placeholder - actual implementation would delete from database
    pass
