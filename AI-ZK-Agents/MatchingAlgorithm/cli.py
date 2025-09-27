import argparse
import json
import sys
from typing import Any, Dict

from .core import match_job_to_candidate
from .utils import canonical_dumps, load_json_or_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="matching",
        description="Compute weighted match score between job requirements and candidate skills; emit ZK-friendly JSON",
    )
    parser.add_argument("--job-id", required=True, help="Job identifier")
    parser.add_argument("--candidate-id", required=True, help="Candidate identifier")
    parser.add_argument(
        "--job-json",
        required=True,
        help="Job requirements either as JSON or path to JSON file. Example: '{"python":0.9,"docker":0.6}'",
    )
    parser.add_argument(
        "--skills-json",
        required=True,
        help="Candidate skills either as JSON or path to JSON file. Example: '{"python":0.8,"docker":0.7}'",
    )
    parser.add_argument("--threshold", type=float, default=0.6, help="Match threshold in [0,1]")

    args = parser.parse_args(argv)

    job_req: Dict[str, float] = load_json_or_path(args.job_json)
    skills: Dict[str, float] = load_json_or_path(args.skills_json)

    res = match_job_to_candidate(
        job_id=args.job_id,
        candidate_id=args.candidate_id,
        job_requirements=job_req,
        user_skills=skills,
        threshold=args.threshold,
    )

    out = res.to_zk_json()
    sys.stdout.write(canonical_dumps(out).decode("utf-8") + "\n")


if __name__ == "__main__":
    main()


