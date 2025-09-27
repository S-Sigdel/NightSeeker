from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from SkillVerification.core import run_for_candidate


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run skill verification once.")
    parser.add_argument("--candidate-id", default="test-candidate")
    parser.add_argument("--resume", action="append", dest="resumes", help="Path to a resume PDF")
    parser.add_argument("--github", help="GitHub username to scan")
    parser.add_argument("--kaggle", action="append", dest="kaggle_urls", help="Kaggle notebook URL")
    args = parser.parse_args()

    result = run_for_candidate(
        candidate_id=args.candidate_id,
        resume_paths=args.resumes,
        github_username=args.github,
        kaggle_urls=args.kaggle_urls,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()