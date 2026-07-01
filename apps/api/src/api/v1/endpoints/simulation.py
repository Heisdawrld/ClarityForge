from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field

from api.v1.endpoints.auth import get_current_user
from services.simulation.engine import (
    DistributionType,
    Outcome,
    SimulationEngine,
    Variable,
    VariableType,
)

router = APIRouter()


class VariableInput(BaseModel):
    name: str = Field(..., description="Variable name for formula reference")
    min_value: float = Field(..., description="Minimum value")
    max_value: float = Field(..., description="Maximum value")
    distribution: DistributionType = Field(default=DistributionType.UNIFORM)
    variable_type: VariableType = Field(default=VariableType.CONTINUOUS)
    mean: float | None = Field(default=None, description="Mean for normal/exponential distribution")
    std_dev: float | None = Field(default=None, description="Standard deviation for normal distribution")
    mode: float | None = Field(default=None, description="Mode for triangular distribution")


class OutcomeInput(BaseModel):
    name: str = Field(..., description="Outcome name")
    formula: str = Field(..., description="Formula using variable names, e.g., 'revenue - costs'")
    variables: list[str] = Field(..., description="List of variable names used in formula")


class SimulationRequest(BaseModel):
    outcome: OutcomeInput
    variables: list[VariableInput]
    iterations: int = Field(default=10000, ge=100, le=100000, description="Number of iterations")
    goal_threshold: float | None = Field(default=None, description="Goal threshold for probability calculation")
    loss_threshold: float | None = Field(default=None, description="Loss threshold for probability calculation")


class SimulationPercentiles(BaseModel):
    p5: float
    p25: float
    median: float
    p75: float
    p95: float


class SimulationResultResponse(BaseModel):
    simulation_id: str
    outcome_name: str
    iterations: int
    mean: float
    std_dev: float
    min: float
    max: float
    percentiles: SimulationPercentiles
    confidence_interval_95: tuple[float, float]
    probability_of_loss: float | None = None
    probability_of_goal: float | None = None


class SensitivityInput(BaseModel):
    outcome: OutcomeInput
    variables: list[VariableInput]
    iterations: int = Field(default=1000, ge=100, le=10000)


class SensitivityItem(BaseModel):
    variable_name: str
    correlation: float
    importance_rank: int


class SensitivityResponse(BaseModel):
    sensitivities: list[SensitivityItem]


@router.post("/simulate", response_model=SimulationResultResponse, status_code=status.HTTP_200_OK)
async def run_simulation(
    request: SimulationRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    engine = SimulationEngine()

    outcome = Outcome(
        name=request.outcome.name,
        formula=request.outcome.formula,
        variables=request.outcome.variables,
    )

    variables = [
        Variable(
            name=v.name,
            min_value=v.min_value,
            max_value=v.max_value,
            distribution=v.distribution,
            variable_type=v.variable_type,
            mean=v.mean,
            std_dev=v.std_dev,
            mode=v.mode,
        )
        for v in request.variables
    ]

    result = engine.run_monte_carlo(
        outcome=outcome,
        variables=variables,
        iterations=request.iterations,
        goal_threshold=request.goal_threshold,
        loss_threshold=request.loss_threshold,
    )

    return SimulationResultResponse(
        simulation_id=result.simulation_id,
        outcome_name=result.outcome_name,
        iterations=result.iterations,
        mean=result.mean,
        std_dev=result.std_dev,
        min=result.min,
        max=result.max,
        percentiles=SimulationPercentiles(
            p5=result.percentile_5,
            p25=result.percentile_25,
            median=result.median,
            p75=result.percentile_75,
            p95=result.percentile_95,
        ),
        confidence_interval_95=result.confidence_interval_95,
        probability_of_loss=result.probability_of_loss,
        probability_of_goal=result.probability_of_goal,
    )


@router.post("/sensitivity", response_model=SensitivityResponse)
async def run_sensitivity_analysis(
    request: SensitivityInput,
    current_user: Annotated[dict, Depends(get_current_user)],
):
    engine = SimulationEngine()

    outcome = Outcome(
        name=request.outcome.name,
        formula=request.outcome.formula,
        variables=request.outcome.variables,
    )

    variables = [
        Variable(
            name=v.name,
            min_value=v.min_value,
            max_value=v.max_value,
            distribution=v.distribution,
            variable_type=v.variable_type,
            mean=v.mean,
            std_dev=v.std_dev,
            mode=v.mode,
        )
        for v in request.variables
    ]

    results = engine.sensitivity_analysis(
        outcome=outcome,
        variables=variables,
        iterations=request.iterations,
    )

    return SensitivityResponse(
        sensitivities=[
            SensitivityItem(
                variable_name=r.variable_name,
                correlation=r.correlation,
                importance_rank=r.importance_rank,
            )
            for r in results
        ]
    )
