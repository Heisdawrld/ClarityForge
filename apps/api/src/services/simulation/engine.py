"""
Monte Carlo Simulation Engine for ClarityForge

Provides what-if scenario modeling with probability ranges and sensitivity analysis.
"""

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from typing import TypedDict

import numpy as np


class DistributionType(str, Enum):
    UNIFORM = "uniform"
    NORMAL = "normal"
    TRIANGULAR = "triangular"
    EXPONENTIAL = "exponential"


class VariableType(str, Enum):
    CONTINUOUS = "continuous"
    DISCRETE = "discrete"


@dataclass
class Variable:
    name: str
    min_value: float
    max_value: float
    distribution: DistributionType = DistributionType.UNIFORM
    variable_type: VariableType = VariableType.CONTINUOUS
    mean: float | None = None
    std_dev: float | None = None
    mode: float | None = None
    probabilities: dict[int, float] | None = None


@dataclass
class Outcome:
    name: str
    formula: str
    variables: list[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    simulation_id: str
    outcome_name: str
    iterations: int
    mean: float
    median: float
    std_dev: float
    min: float
    max: float
    percentile_5: float
    percentile_25: float
    percentile_75: float
    percentile_95: float
    confidence_interval_95: tuple[float, float]
    probability_of_loss: float | None = None
    probability_of_goal: float | None = None


@dataclass
class SensitivityResult:
    variable_name: str
    correlation: float
    importance_rank: int


class SimulationEngine:
    def __init__(self, seed: int | None = None):
        self.rng = np.random.default_rng(seed)

    def run_monte_carlo(
        self,
        outcome: Outcome,
        variables: list[Variable],
        iterations: int = 10000,
        goal_threshold: float | None = None,
        loss_threshold: float | None = None,
    ) -> SimulationResult:
        if not variables:
            raise ValueError("At least one variable is required")

        samples = self._generate_samples(variables, iterations)
        outcome_values = self._evaluate_outcome(outcome, samples)

        result = SimulationResult(
            simulation_id=str(uuid.uuid4()),
            outcome_name=outcome.name,
            iterations=iterations,
            mean=float(np.mean(outcome_values)),
            median=float(np.median(outcome_values)),
            std_dev=float(np.std(outcome_values)),
            min=float(np.min(outcome_values)),
            max=float(np.max(outcome_values)),
            percentile_5=float(np.percentile(outcome_values, 5)),
            percentile_25=float(np.percentile(outcome_values, 25)),
            percentile_75=float(np.percentile(outcome_values, 75)),
            percentile_95=float(np.percentile(outcome_values, 95)),
            confidence_interval_95=self._confidence_interval(outcome_values, 0.95),
        )

        if loss_threshold is not None:
            result.probability_of_loss = float(np.mean(outcome_values < loss_threshold))

        if goal_threshold is not None:
            result.probability_of_goal = float(np.mean(outcome_values >= goal_threshold))

        return result

    def sensitivity_analysis(
        self,
        outcome: Outcome,
        variables: list[Variable],
        iterations: int = 1000,
    ) -> list[SensitivityResult]:
        samples = self._generate_samples(variables, iterations)
        outcome_values = self._evaluate_outcome(outcome, samples)

        sensitivities = []
        for i, var in enumerate(variables):
            correlation = float(np.corrcoef(samples[i], outcome_values)[0, 1])
            sensitivities.append(
                SensitivityResult(
                    variable_name=var.name,
                    correlation=correlation if not np.isnan(correlation) else 0.0,
                    importance_rank=0,
                )
            )

        sensitivities.sort(key=lambda x: abs(x.correlation), reverse=True)
        for i, s in enumerate(sensitivities):
            s.importance_rank = i + 1

        return sensitivities

    def _generate_samples(self, variables: list[Variable], iterations: int) -> list[np.ndarray]:
        samples = []
        for var in variables:
            samples.append(self._sample_variable(var, iterations))
        return samples

    def _sample_variable(self, variable: Variable, iterations: int) -> np.ndarray:
        size = (iterations,)

        if variable.distribution == DistributionType.UNIFORM:
            return self.rng.uniform(variable.min_value, variable.max_value, size)

        elif variable.distribution == DistributionType.NORMAL:
            mean = variable.mean if variable.mean is not None else (variable.min_value + variable.max_value) / 2
            std = variable.std_dev if variable.std_dev is not None else (variable.max_value - variable.min_value) / 6
            return self.rng.normal(mean, std, size)

        elif variable.distribution == DistributionType.TRIANGULAR:
            mode = variable.mode if variable.mode is not None else (variable.min_value + variable.max_value) / 2
            return self.rng.triangular(variable.min_value, mode, variable.max_value, size)

        elif variable.distribution == DistributionType.EXPONENTIAL:
            scale = 1.0 / (variable.mean if variable.mean else 1.0)
            return self.rng.exponential(scale, size)

        return self.rng.uniform(variable.min_value, variable.max_value, size)

    def _evaluate_outcome(self, outcome: Outcome, samples: list[np.ndarray]) -> np.ndarray:
        formula = outcome.formula
        for i, var_name in enumerate(outcome.variables):
            formula = formula.replace(var_name, f"samples[{i}]")

        try:
            result = eval(formula, {"samples": samples, "np": np})
            if isinstance(result, np.ndarray):
                return result
            return np.array([result])
        except Exception as e:
            raise ValueError(f"Error evaluating formula: {e}")

    def _confidence_interval(self, values: np.ndarray, confidence: float) -> tuple[float, float]:
        alpha = 1 - confidence
        mean = np.mean(values)
        stderr = np.std(values) / np.sqrt(len(values))
        margin = stderr * 1.96
        return (float(mean - margin), float(mean + margin))
