"""Run a reproducible single-agent experiment and persist an auditable artifact."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agents.agent_builder import agent_builder  # noqa: E402
from agents.platform_manager import platform_manager  # noqa: E402
from agents.web_search import web_search  # noqa: E402
from config.experiment import ExperimentConfig  # noqa: E402
from tools.experiment_metrics import compute_response_metrics  # noqa: E402

LOGGER = logging.getLogger("experiment")

AGENTS = {
    "agent-builder": agent_builder,
    "platform-manager": platform_manager,
    "web-search": web_search,
}


def _artifact_path(artifacts_dir: Path) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return artifacts_dir / f"run-{timestamp}.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-id", dest="agent_id", help="Agent id to run (web-search, platform-manager, agent-builder)")
    parser.add_argument("--task-input", dest="task_input", help="Prompt/input sent to the selected agent")
    parser.add_argument("--model", dest="model", help="Requested model label recorded in run metadata for auditing")
    parser.add_argument("--temperature", type=float, help="Requested temperature recorded in run metadata for auditing")
    parser.add_argument("--seed", type=int, help="Integer seed recorded in run metadata for reproducibility tracking")
    parser.add_argument("--dataset", dest="dataset", help="Dataset or experiment cohort label written into artifacts")
    parser.add_argument("--session-id", dest="session_id", help="Session id used for the agent run")
    parser.add_argument("--artifacts-dir", type=Path, help="Directory where run artifacts are saved")
    parser.add_argument("--dry-run", action="store_true", help="Write an artifact without calling model/tools")
    return parser.parse_args()


def _write_artifact(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    args = parse_args()
    config = ExperimentConfig.from_env().with_overrides(
        agent_id=args.agent_id,
        task_input=args.task_input,
        model=args.model,
        temperature=args.temperature,
        seed=args.seed,
        dataset=args.dataset,
        session_id=args.session_id,
        artifacts_dir=args.artifacts_dir,
    )

    if config.agent_id not in AGENTS:
        print(f"Unsupported --agent-id '{config.agent_id}'. Choose one of: {', '.join(sorted(AGENTS))}", file=sys.stderr)
        return 1

    artifact_file = _artifact_path(config.artifacts_dir)
    base_payload: dict[str, object] = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "status": "pending",
        "params": {
            "agent_id": config.agent_id,
            "task_input": config.task_input,
            "model": config.model,
            "temperature": config.temperature,
            "seed": config.seed,
            "dataset": config.dataset,
            "session_id": config.session_id,
        },
    }

    if args.dry_run:
        base_payload["status"] = "dry_run"
        _write_artifact(artifact_file, base_payload)
        LOGGER.info("Dry run complete: artifact=%s", artifact_file)
        return 0

    agent = AGENTS[config.agent_id]
    try:
        run_output = agent.run(
            config.task_input,
            session_id=config.session_id,
            metadata={
                "dataset": config.dataset,
                "seed": config.seed,
                "requested_model": config.model,
                "requested_temperature": config.temperature,
            },
        )
        response_text = run_output.get_content_as_string()
        base_payload["status"] = "completed"
        base_payload["response"] = response_text
        base_payload["metrics"] = compute_response_metrics(response_text)
        _write_artifact(artifact_file, base_payload)
        LOGGER.info("Experiment completed: artifact=%s", artifact_file)
        return 0
    except Exception as exc:  # pragma: no cover - runtime failure path
        base_payload["status"] = "failed"
        base_payload["error"] = str(exc)
        _write_artifact(artifact_file, base_payload)
        LOGGER.exception("Experiment failed: artifact=%s", artifact_file)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
