from __future__ import annotations

from typing import Dict

from .utils import ReputationResult, derive_secret


def clamp01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def adjust_reputation(
    worker_id: str,
    base_reputation: float,
    job_complexity: float,
    employer_rating: float,
    verified_projects: int,
) -> ReputationResult:
    base = clamp01(base_reputation)
    complexity = clamp01(job_complexity)
    rating = clamp01(employer_rating)
    projects = max(0, int(verified_projects))

    # Heuristic adjustment rule:
    # - complexity amplifies gains
    # - employer rating moderates adjustment
    # - more verified projects add diminishing returns
    project_factor = 1.0 - (0.5 ** max(1, projects))  # in (0,1)
    adjustment = 0.4 * complexity + 0.4 * rating + 0.2 * project_factor
    new_rep = clamp01(0.7 * base + 0.3 * adjustment)

    details: Dict[str, float] = {
        "base": round(base, 6),
        "complexity": round(complexity, 6),
        "employer_rating": round(rating, 6),
        "project_factor": round(project_factor, 6),
        "adjustment": round(adjustment, 6),
    }

    worker_secret = derive_secret("worker", {"worker_id": worker_id, "base_reputation": base})
    adjustment_secret = derive_secret("adjustment", {
        "worker_id": worker_id,
        "job_complexity": complexity,
        "employer_rating": rating,
        "verified_projects": projects,
        "new_reputation": new_rep,
    })

    return ReputationResult(
        worker_id=worker_id,
        base_reputation=base,
        job_complexity=complexity,
        employer_rating=rating,
        verified_projects=projects,
        new_reputation=new_rep,
        details=details,
        worker_secret=worker_secret,
        adjustment_secret=adjustment_secret,
    )


