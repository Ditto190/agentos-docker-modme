"""Typed configuration for experiment and evaluation scripts."""

from __future__ import annotations

from dataclasses import dataclass, replace
from os import getenv
from pathlib import Path

DEFAULT_AGENT_ID = "web-search"
DEFAULT_TASK_INPUT = "What is AgentOS and what can it do?"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_TEMPERATURE = 0.0
DEFAULT_SEED = 42
DEFAULT_DATASET = "manual"
DEFAULT_SESSION_ID = "research-session"
DEFAULT_ARTIFACTS_DIR = Path("artifacts")


@dataclass(frozen=True)
class ExperimentConfig:
    agent_id: str = DEFAULT_AGENT_ID
    task_input: str = DEFAULT_TASK_INPUT
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    seed: int = DEFAULT_SEED
    dataset: str = DEFAULT_DATASET
    session_id: str = DEFAULT_SESSION_ID
    artifacts_dir: Path = DEFAULT_ARTIFACTS_DIR

    @classmethod
    def from_env(cls) -> "ExperimentConfig":
        temperature_raw = getenv("EXPERIMENT_TEMPERATURE", str(DEFAULT_TEMPERATURE))
        seed_raw = getenv("EXPERIMENT_SEED", str(DEFAULT_SEED))
        try:
            temperature = float(temperature_raw)
        except ValueError as exc:
            raise ValueError(f"EXPERIMENT_TEMPERATURE must be a float, got: {temperature_raw!r}") from exc
        try:
            seed = int(seed_raw)
        except ValueError as exc:
            raise ValueError(f"EXPERIMENT_SEED must be an integer, got: {seed_raw!r}") from exc
        return cls(
            agent_id=getenv("EXPERIMENT_AGENT_ID", DEFAULT_AGENT_ID),
            task_input=getenv("EXPERIMENT_TASK_INPUT", DEFAULT_TASK_INPUT),
            model=getenv("EXPERIMENT_MODEL", DEFAULT_MODEL),
            temperature=temperature,
            seed=seed,
            dataset=getenv("EXPERIMENT_DATASET", DEFAULT_DATASET),
            session_id=getenv("EXPERIMENT_SESSION_ID", DEFAULT_SESSION_ID),
            artifacts_dir=Path(getenv("EXPERIMENT_ARTIFACTS_DIR", str(DEFAULT_ARTIFACTS_DIR))),
        )

    def with_overrides(
        self,
        *,
        agent_id: str | None = None,
        task_input: str | None = None,
        model: str | None = None,
        temperature: float | None = None,
        seed: int | None = None,
        dataset: str | None = None,
        session_id: str | None = None,
        artifacts_dir: Path | None = None,
    ) -> "ExperimentConfig":
        return replace(
            self,
            agent_id=self.agent_id if agent_id is None else agent_id,
            task_input=self.task_input if task_input is None else task_input,
            model=self.model if model is None else model,
            temperature=self.temperature if temperature is None else temperature,
            seed=self.seed if seed is None else seed,
            dataset=self.dataset if dataset is None else dataset,
            session_id=self.session_id if session_id is None else session_id,
            artifacts_dir=self.artifacts_dir if artifacts_dir is None else artifacts_dir,
        )
