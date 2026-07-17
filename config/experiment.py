"""Typed configuration for experiment and evaluation scripts."""

from __future__ import annotations

from dataclasses import dataclass, replace
from os import getenv
from pathlib import Path


@dataclass(frozen=True)
class ExperimentConfig:
    agent_id: str = "web-search"
    task_input: str = "What is AgentOS and what can it do?"
    model: str = "gpt-5.6-sol"
    temperature: float = 0.0
    seed: int = 42
    dataset: str = "manual"
    session_id: str = "research-session"
    artifacts_dir: Path = Path("artifacts")

    @classmethod
    def from_env(cls) -> "ExperimentConfig":
        return cls(
            agent_id=getenv("EXPERIMENT_AGENT_ID", cls.agent_id),
            task_input=getenv("EXPERIMENT_TASK_INPUT", cls.task_input),
            model=getenv("EXPERIMENT_MODEL", cls.model),
            temperature=float(getenv("EXPERIMENT_TEMPERATURE", str(cls.temperature))),
            seed=int(getenv("EXPERIMENT_SEED", str(cls.seed))),
            dataset=getenv("EXPERIMENT_DATASET", cls.dataset),
            session_id=getenv("EXPERIMENT_SESSION_ID", cls.session_id),
            artifacts_dir=Path(getenv("EXPERIMENT_ARTIFACTS_DIR", str(cls.artifacts_dir))),
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
