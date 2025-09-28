import math
from .config import WEIGHTS, MAX_EXPECTED
from .utils import months_since
from .llm_utils import llm_explain_score

def _snippet(e):
    src = e.get("source", "")
    typ = e.get("type", "")
    if src == "github":
        repo = e.get("repo", "")
        detail = e.get("detail", "")
        f = e.get("file", "")
        return f"gh:{repo} {typ} {detail} {f}".strip()
    if src == "kaggle":
        return f"kaggle:{e.get('type','')} {e.get('detail','')}"
    if src == "resume":
        return f"resume:{e.get('type','')}"
    return f"{src}:{typ}"

def _score_github(evidences):
    s = 0.0
    for e in evidences:
        typ = e.get("type", "")
        base = 0.6
        if typ == "language":
            base = 0.9
        elif typ == "import":
            base = 0.8
        elif typ == "dependency_file":
            base = 0.5
        elif typ == "readme":
            base = 0.3
        loc = max(10, int(e.get("loc", 10)))
        loc_factor = min(1.0, math.log(loc) / MAX_EXPECTED)
        recency = e.get("recency")
        if recency:
            m = months_since(recency)
            recency_factor = max(0.35, 1.0 - (m / 60.0))
        else:
            recency_factor = 0.7
        s += base * loc_factor * recency_factor
    return s

def _score_kaggle(evidences):
    count = len(evidences)
    return min(1.0, count / 8.0)

def _score_resume(evidences):
    s = 0.0
    for e in evidences:
        typ = e.get("type", "")
        s += 0.6 if typ == "resume_skills_section" else 0.35
    return min(1.0, s / 3.0)

def aggregate_and_score(skills_map, resume_skills):
    results = []
    for skill, evids in skills_map.items():
        gh = [e for e in evids if e.get("source") == "github"]
        kg = [e for e in evids if e.get("source") == "kaggle"]
        rs = [e for e in evids if e.get("source") == "resume"]

        repo_signal = _score_github(gh)
        nb_signal = _score_kaggle(kg)
        res_signal = _score_resume(rs)

        repo_conf = 100.0 * WEIGHTS.get("repo", 0.6) * min(1.0, repo_signal / 6.0)
        nb_conf   = 100.0 * WEIGHTS.get("notebook", 0.25) * nb_signal
        res_conf  = 100.0 * WEIGHTS.get("resume", 0.15) * res_signal

        base_conf = round(min(100.0, repo_conf + nb_conf + res_conf))

        snippets = []
        for e in (gh + kg + rs):
            sn = _snippet(e)
            if sn and sn not in snippets:
                snippets.append(sn)

        adj, explain = llm_explain_score(skill, snippets, int(base_conf))
        final_conf = max(0, min(100, int(base_conf + adj)))

        results.append({
            "skill": skill,
            "confidence": final_conf,
            "evidence": snippets[:12],
            "llm_explain": explain
        })
    results.sort(key=lambda r: r["confidence"], reverse=True)
    return results