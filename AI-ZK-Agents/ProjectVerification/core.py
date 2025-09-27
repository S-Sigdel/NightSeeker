from __future__ import annotations

from typing import Dict

from .utils import (
    VerificationResult,
    commitment_from_secret,
    derive_secret,
    score_repo_against_requirements,
)


def verify_submission(
    job_id: str,
    submission_id: str,
    worker_id: str,
    repo_path: str,
    job_requirements: Dict[str, float],
    threshold: float = 0.7,
) -> VerificationResult:
    coverage, details = score_repo_against_requirements(repo_path, job_requirements)
    passed = coverage >= threshold

    job_secret = derive_secret("job", {"job_id": job_id, "requirements": details["requirements"]})
    submission_secret = derive_secret("submission", {
        "submission_id": submission_id,
        "worker_id": worker_id,
        "repo": details["repo"],
        "detected_skills": details["detected_skills"],
    })
    # nullifier derived from tuple (job, submission) to prevent double-release
    nullifier_secret = derive_secret("nullifier", {"job_id": job_id, "submission_id": submission_id, "worker_id": worker_id})

    return VerificationResult(
        job_id=job_id,
        submission_id=submission_id,
        worker_id=worker_id,
        coverage=coverage,
        passed=passed,
        threshold=threshold,
        details=details,
        job_secret=job_secret,
        submission_secret=submission_secret,
        nullifier_secret=nullifier_secret,
    )


