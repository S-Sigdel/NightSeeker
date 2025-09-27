from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, Tuple

from .utils import (
    MatchResult,
    derive_secret,
    normalize_skill_name,
)


def compute_weighted_overlap(
    job_requirements: Mapping[str, float],
    user_skills: Mapping[str, float],
) -> Tuple[float, Dict[str, Any]]:
    """Compute a symmetric weighted overlap score and provide per-skill details.

    - job_requirements: map of normalized skill -> weight in [0,1]
    - user_skills: map of normalized skill -> confidence in [0,1]

    Score formula (bounded in [0,1]):
        sum_over_s ( min(job_w[s], user_c[s]) ) / sum_over_s ( job_w[s] )

    Returns:
        (score, details)
    """
    # Normalize keys
    jr = {normalize_skill_name(k): max(0.0, min(1.0, float(v))) for k, v in job_requirements.items()}
    us = {normalize_skill_name(k): max(0.0, min(1.0, float(v))) for k, v in user_skills.items()}

    denom = sum(jr.values()) or 1.0
    overlap_sum = 0.0
    per_skill: List[Dict[str, Any]] = []
    for skill, job_w in jr.items():
        conf = us.get(skill, 0.0)
        contrib = min(job_w, conf)
        overlap_sum += contrib
        per_skill.append({
            "skill": skill,
            "job_weight": round(job_w, 6),
            "user_confidence": round(conf, 6),
            "contribution": round(contrib, 6),
        })

    score = overlap_sum / denom
    details = {
        "normalized": {
            "job_requirements": jr,
            "user_skills": us,
        },
        "per_skill": per_skill,
        "overlap_sum": round(overlap_sum, 6),
        "denominator": round(denom, 6),
    }
    return score, details


def match_job_to_candidate(
    job_id: str,
    candidate_id: str,
    job_requirements: Mapping[str, float],
    user_skills: Mapping[str, float],
    threshold: float = 0.6,
) -> MatchResult:
    score, details = compute_weighted_overlap(job_requirements, user_skills)
    is_match = score >= threshold

    job_secret = derive_secret("job", {"job_id": job_id, "requirements": details["normalized"]["job_requirements"]})
    skills_secret = derive_secret("skills", {"candidate_id": candidate_id, "skills": details["normalized"]["user_skills"]})
    match_secret = derive_secret("match", {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "score": round(score, 6),
        "threshold": threshold,
        "is_match": is_match,
    })

    return MatchResult(
        job_id=job_id,
        candidate_id=candidate_id,
        score=score,
        is_match=is_match,
        threshold=threshold,
        details=details,
        job_secret=job_secret,
        skills_secret=skills_secret,
        match_secret=match_secret,
    )


