import json
from collections import defaultdict
from datetime import datetime
from .resume_parser import parse_resume_pdf_bytes, extract_skills_from_resume_text
from .github_analyzer import analyze_github_user
from .kaggle_analyzer import analyze_kaggle_notebook
from .llm_utils import canonicalize_skills_with_embeddings
from .scoring import aggregate_and_score
from .config import BASE_SKILL_LEXICON

def run_for_candidate(candidate_id, resume_paths=None, github_username=None, kaggle_urls=None):
    skills_map = defaultdict(list)
    resume_skills = []

    # Resume
    if resume_paths:
        for p in resume_paths:
            with open(p, "rb") as fh:
                text = parse_resume_pdf_bytes(fh.read())
                rs = extract_skills_from_resume_text(text)
                resume_skills.extend(rs)
                for s,src in rs:
                    skills_map[s].append({"source":"resume", "type": src})

    # GitHub
    if github_username:
        gh = analyze_github_user(github_username)
        for s, evids in gh.items():
            skills_map[s].extend(evids)

    # Kaggle
    if kaggle_urls:
        for u in kaggle_urls:
            kg = analyze_kaggle_notebook(u)
            for s, evid in kg.items():
                skills_map[s].extend(evid)

    # Canonicalize into allowed skills only
    all_tokens = list(skills_map.keys())
    if all_tokens:
        allowed = set(BASE_SKILL_LEXICON.values())
        canonical_map = canonicalize_skills_with_embeddings(all_tokens, allowed_canonical=allowed)
        new_map = defaultdict(list)
        for tok, evids in skills_map.items():
            cm = canonical_map.get(tok)
            if not cm:
                continue  # drop tokens that don't map to allowed skills
            canonical = cm["canonical_name"]
            new_map[canonical].extend(evids)
        skills_map = new_map

    # Score
    scored = aggregate_and_score(skills_map, resume_skills)
    out = {
        "id": candidate_id,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "skills": [
            {
                "id": f"{candidate_id}:{i+1}",
                "skill": r["skill"],
                "confidence": r["confidence"],
                "evidence": r["evidence"],
                "llm_explain": r["llm_explain"]
            }
            for i, r in enumerate(scored)
        ]
    }
    return out