from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field

from api.v1.endpoints.auth import get_current_user
from services.export.generator import (
    ExportFormat,
    ExportService,
    ExportResult,
    ReasoningData,
    SharePermission,
)

router = APIRouter()


class ExportRequest(BaseModel):
    session_id: str = Field(..., description="Session ID to export")
    format: ExportFormat = Field(default=ExportFormat.MARKDOWN)
    include_evidence: bool = Field(default=True, description="Include evidence in export")
    include_questions: bool = Field(default=True, description="Include questions in export")


class CollaborativeLinkRequest(BaseModel):
    session_id: str = Field(..., description="Session ID to share")
    permission: SharePermission = Field(default=SharePermission.VIEW_ONLY)
    expires_in_hours: int | None = Field(default=None, ge=1, le=720, description="Link expiration in hours")


class CollaborativeLinkResponse(BaseModel):
    link_id: str
    access_url: str
    permission: str
    created_at: str
    expires_at: str | None


@router.post("/export")
async def export_session(
    request: ExportRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    service = ExportService()
    
    # Placeholder - would fetch actual session data
    # For now, return a sample structure
    sample_data = ReasoningData(
        title="Sample Reasoning Session",
        input_text="Sample input text for demonstration",
        assumptions=[
            {"text": "Sample assumption 1", "isExplicit": True, "confidence": 0.9},
            {"text": "Sample assumption 2", "isExplicit": False, "confidence": 0.6},
        ],
        biases=[
            {
                "name": "Confirmation Bias",
                "type": "confirmation",
                "description": "Tendency to search for confirming evidence",
                "mitigation": "Actively seek opposing viewpoints",
                "severity": "medium",
            }
        ],
        confidence_score=0.75,
        created_at="2024-01-01T00:00:00Z",
    )

    result = service.export_markdown(sample_data)

    if request.format == ExportFormat.MARKDOWN:
        return Response(
            content=result.content,
            media_type="text/markdown",
            headers={
                "Content-Disposition": f'attachment; filename="clarityforge-{request.session_id}.md"'
            },
        )
    elif request.format == ExportFormat.JSON:
        result = service.export_json(sample_data)
        return Response(
            content=result.content,
            media_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="clarityforge-{request.session_id}.json"'
            },
        )
    elif request.format == ExportFormat.PDF:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="PDF generation requires additional configuration. Use markdown export for now.",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Unsupported format: {request.format}",
    )


@router.post("/share", response_model=CollaborativeLinkResponse)
async def create_share_link(
    request: CollaborativeLinkRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    service = ExportService()

    link = service.create_collaborative_link(
        session_id=request.session_id,
        permission=request.permission,
        expires_in_hours=request.expires_in_hours,
    )

    return CollaborativeLinkResponse(
        link_id=link.link_id,
        access_url=link.access_url or "",
        permission=link.permission.value,
        created_at=link.created_at,
        expires_at=link.expires_at,
    )


@router.get("/share/{link_id}")
async def get_shared_session(
    link_id: str,
):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Collaborative links require additional infrastructure setup",
    )
