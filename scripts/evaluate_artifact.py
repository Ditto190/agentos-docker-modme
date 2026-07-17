"""Evaluate experiment artifacts and persist metric summaries."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.experiment_metrics import compute_response_metrics  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path, help="Path to an experiment JSON artifact")
    parser.add_argument("--output", type=Path, help="Path for evaluation output JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload = json.loads(args.artifact.read_text(encoding="utf-8"))
    response_text = str(payload.get("response", ""))
    metrics = compute_response_metrics(response_text)

    summary = {
        "artifact": str(args.artifact),
        "evaluated_at_utc": datetime.now(UTC).isoformat(),
        "status": payload.get("status", "unknown"),
        "metric": "non_empty_response",
        "score": metrics["non_empty_response"],
        "metrics": metrics,
    }

    output_path = args.output or args.artifact.with_name(f"eval-{args.artifact.name}")
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
