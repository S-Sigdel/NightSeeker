import argparse
import sys

from .core import adjust_reputation
from .utils import canonical_dumps


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="reputation-adjustment",
        description="Adjust reputation from job complexity, employer rating, and verified projects; emit ZK-friendly JSON",
    )
    parser.add_argument("--worker-id", required=True)
    parser.add_argument("--base-reputation", type=float, required=True)
    parser.add_argument("--job-complexity", type=float, required=True)
    parser.add_argument("--employer-rating", type=float, required=True)
    parser.add_argument("--verified-projects", type=int, required=True)

    args = parser.parse_args(argv)

    res = adjust_reputation(
        worker_id=args.worker_id,
        base_reputation=args.base_reputation,
        job_complexity=args.job_complexity,
        employer_rating=args.employer_rating,
        verified_projects=args.verified_projects,
    )

    out = res.to_zk_json()
    sys.stdout.write(canonical_dumps(out).decode("utf-8") + "\n")


if __name__ == "__main__":
    main()


