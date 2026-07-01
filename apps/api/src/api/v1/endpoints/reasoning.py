from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from api.v1.endpoints.auth import get_current_user
from services.reasoning.pipeline import ReasoningPipeline

router = APIRouter()


class ReasoningInput(BaseModel):
    text: str = Field(..., min_length=10, description="The text to analyze")
    include_evidence: bool = Field(default=True, description="Include real-time evidence search")
    bias_types: list[str] | None = Field(default=None, description="Specific bias types to check")


class AssumptionResponse(BaseModel):
    id: str
    text: str
    is_explicit: bool
    confidence: float


class BiasFlagResponse(BaseModel):
    id: str
    type: str
    name: str
    description: str
    severity: str
    mitigation: str


class EvidenceResponse(BaseModel):
    id: str
    content: str
    source: str
    url: str | None
    relevance: float
    polarity: str


class AlternativeResponse(BaseModel):
    id: str
    perspective: str
    reasoning: str
    strength: float


class QuestionResponse(BaseModel):
    id: str
    text: str
    priority: str
    category: str


class ReasoningOutputResponse(BaseModel):
    assumptions: list[AssumptionResponse]
    biases: list[BiasFlagResponse]
    evidence: list[EvidenceResponse]
    alternatives: list[AlternativeResponse]
    questions: list[QuestionResponse]
    confidence_score: float


class ReasoningResponse(BaseModel):
    output: ReasoningOutputResponse


@router.post("/analyze", response_model=ReasoningResponse, status_code=status.HTTP_200_OK)
async def analyze_reasoning(
    input_data: ReasoningInput,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    pipeline = ReasoningPipeline()
    
    result = await pipeline.process(
        text=input_data.text,
        include_evidence=input_data.include_evidence,
        bias_types=input_data.bias_types,
    )
    
    return ReasoningResponse(output=result)


@router.get("/biases")
async def list_biases(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    from services.bias.taxonomy import BIAS_TAXONOMY
    
    return {
        "biases": [
            {
                "type": bias.type,
                "name": bias.name,
                "description": bias.description,
                "examples": bias.examples,
                "mitigation": bias.mitigation,
            }
            for bias in BIAS_TAXONOMY
        ]
    }
