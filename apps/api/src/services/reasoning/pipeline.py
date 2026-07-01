import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from services.bias.taxonomy import BIAS_TAXONOMY

if TYPE_CHECKING:
    from services.ai.providers import AIProvider


class Assumption(BaseModel):
    id: str
    text: str
    is_explicit: bool
    confidence: float


class BiasFlag(BaseModel):
    id: str
    type: str
    name: str
    description: str
    severity: str
    mitigation: str


class Evidence(BaseModel):
    id: str
    content: str
    source: str
    url: str | None = None
    relevance: float
    polarity: str


class Alternative(BaseModel):
    id: str
    perspective: str
    reasoning: str
    strength: float


class Question(BaseModel):
    id: str
    text: str
    priority: str
    category: str


class ReasoningOutput(BaseModel):
    assumptions: list[Assumption] = Field(default_factory=list)
    biases: list[BiasFlag] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    alternatives: list[Alternative] = Field(default_factory=list)
    questions: list[Question] = Field(default_factory=list)
    confidence_score: float


class ReasoningPipeline:
    def __init__(self, ai_provider: "AIProvider | None" = None):
        self.ai_provider = ai_provider

    async def process(
        self,
        text: str,
        include_evidence: bool = True,
        bias_types: list[str] | None = None,
    ) -> ReasoningOutput:
        output = ReasoningOutput()

        # Step 1: Extract assumptions
        output.assumptions = await self._extract_assumptions(text)

        # Step 2: Detect biases
        output.biases = await self._detect_biases(text, output.assumptions, bias_types)

        # Step 3: Find evidence (if enabled)
        if include_evidence:
            output.evidence = await self._search_evidence(text, output.biases)

        # Step 4: Generate alternatives
        output.alternatives = await self._generate_alternatives(text, output.assumptions)

        # Step 5: Generate questions
        output.questions = await self._generate_questions(text, output.biases)

        # Step 6: Calculate confidence
        output.confidence_score = self._calculate_confidence(output)

        return output

    async def _extract_assumptions(self, text: str) -> list[Assumption]:
        # Placeholder - would use AI to extract assumptions
        assumptions = [
            Assumption(
                id=str(uuid.uuid4()),
                text="Implicit assumption detected in the reasoning",
                is_explicit=False,
                confidence=0.7,
            )
        ]
        return assumptions

    async def _detect_biases(
        self,
        text: str,
        assumptions: list[Assumption],
        bias_types: list[str] | None = None,
    ) -> list[BiasFlag]:
        # Placeholder - would use AI to detect biases
        detected_biases = []
        for bias in BIAS_TAXONOMY[:3]:
            detected_biases.append(
                BiasFlag(
                    id=str(uuid.uuid4()),
                    type=bias.type,
                    name=bias.name,
                    description=bias.description,
                    severity="medium",
                    mitigation=bias.mitigation,
                )
            )
        return detected_biases

    async def _search_evidence(self, text: str, biases: list[BiasFlag]) -> list[Evidence]:
        # Placeholder - would use Tavily API
        return []

    async def _generate_alternatives(self, text: str, assumptions: list[Assumption]) -> list[Alternative]:
        # Placeholder - would use AI to generate alternatives
        return []

    async def _generate_questions(self, text: str, biases: list[BiasFlag]) -> list[Question]:
        # Placeholder - would use AI to generate questions
        return [
            Question(
                id=str(uuid.uuid4()),
                text="What evidence would contradict this reasoning?",
                priority="high",
                category="evidence",
            )
        ]

    def _calculate_confidence(self, output: ReasoningOutput) -> float:
        base_score = 0.5
        if output.biases:
            base_score -= 0.1 * len(output.biases)
        if output.assumptions:
            avg_confidence = sum(a.confidence for a in output.assumptions) / len(output.assumptions)
            base_score = (base_score + avg_confidence) / 2
        return max(0.0, min(1.0, base_score))
