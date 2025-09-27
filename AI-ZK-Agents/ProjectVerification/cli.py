import argparse
import json
import sys
from typing import Dict

from .core import verify_submission
from .utils import canonical_dumps


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="project-verification",
        description="Validate a repo against job requirements; emit ZK-friendly JSON with commitments and nullifier",
    )
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--submission-id", required=True)
    parser.add_argument("--worker-id", required=True)
    parser.add_argument("--repo-path", required=True)
    parser.add_argument("--requirements-json", required=True, help="JSON or path to JSON for job requirements")
    parser.add_argument("--threshold", type=float, default=0.7)

    args = parser.parse_args(argv)

    # Accept either path or inline JSON
    try:
        if args.requirements_json.strip().startswith("{"):
            req: Dict[str, float] = json.loads(args.requirements_json)
        else:
            with open(args.requirements_json, "r", encoding="utf-8") as fh:
                req = json.load(fh)
    except Exception as e:
        raise SystemExit(f"Failed to load requirements-json: {e}")

    res = verify_submission(
        job_id=args.job_id,
        submission_id=args.submission_id,
        worker_id=args.worker_id,
        repo_path=args.repo_path,
        job_requirements=req,
        threshold=args.threshold,
    )

    out = res.to_zk_json()
    sys.stdout.write(canonical_dumps(out).decode("utf-8") + "\n")


if __name__ == "__main__":
    main()


