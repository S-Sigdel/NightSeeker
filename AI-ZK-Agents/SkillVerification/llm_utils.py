import time, json, math
import openai
from .config import EMBED_MODEL, LLM_MODEL, USE_OPENAI, BASE_SKILL_LEXICON

def get_embedding(text):
    resp = openai.Embeddings.create(model=EMBED_MODEL, input=text)
    return resp["data"][0]["embedding"]

def cosine_sim(a,b):
    dot = sum(x*y for x,y in zip(a,b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na==0 or nb==0: return 0.0
    return dot/(na*nb)

def canonicalize_skills_with_embeddings(skill_tokens, allowed_canonical=None):
    allowed = set(allowed_canonical or BASE_SKILL_LEXICON.values())

    if not USE_OPENAI:
        # Keep only tokens already in allowed
        return {
            t: {"canonical_name": t, "synonyms": [t], "rationale": "in lexicon"}
            for t in skill_tokens if t in allowed
        }

    embeddings = {}
    for t in skill_tokens:
        embeddings[t] = get_embedding(t)
        time.sleep(0.1)

    clusters, used = [], set()
    for t in skill_tokens:
        if t in used: continue
        cluster = [t]; used.add(t)
        for u in skill_tokens:
            if u in used: continue
            if cosine_sim(embeddings[t], embeddings[u]) > 0.86:
                cluster.append(u)
                used.add(u)
        clusters.append(cluster)

    canonical_map = {}
    allowed_list = sorted(list(allowed))
    for c in clusters:
        prompt = (
            "You normalize raw tech tokens into a fixed skill list.\n"
            f"Allowed skills ONLY: {allowed_list}\n"
            f"Tokens: {c}\n"
            "Return JSON: {\"canonical_name\": <one of allowed or NONE>, \"synonyms\": [...], \"rationale\": \"...\"}"
        )
        resp = openai.ChatCompletion.create(
            model=LLM_MODEL,
            messages=[
                {"role":"system","content":"Choose the closest allowed canonical skill or NONE if no match."},
                {"role":"user","content":prompt}
            ],
            max_tokens=200,
            temperature=0.0
        )
        txt = resp["choices"][0]["message"]["content"]
        try:
            j = json.loads(txt)
            name = j.get("canonical_name")
            if name in allowed:
                for token in c:
                    canonical_map[token] = j
            # else drop cluster (no mapping)
        except Exception:
            # drop cluster on parse error
            pass

    return canonical_map

def llm_explain_score(skill, evidence_snippets, base_confidence):
    if not USE_OPENAI:
        return 0, "no LLM adjustment"

    prompt = (
        f"Skill: {skill}\n\n"
        f"Evidence (short list):\n" + "\n".join(evidence_snippets[:8]) + "\n\n"
        f"Current confidence (0-100): {base_confidence}\n\n"
        "Return JSON: {\"adjust\": <int -10..10>, \"explain\": \"one-sentence reason for adjust\"}."
    )
    resp = openai.ChatCompletion.create(
        model=LLM_MODEL,
        messages=[
            {"role":"system","content":"You are an objective tech evaluator. Suggest small numeric adjustments (-10..10) to a confidence score and explain briefly."},
            {"role":"user","content":prompt}
        ],
        max_tokens=120,
        temperature=0.0
    )
    txt = resp["choices"][0]["message"]["content"]
    try:
        j = json.loads(txt)
        adj = int(j.get("adjust",0))
        explain = j.get("explain","")
    except Exception:
        adj, explain = 0, "no LLM adjustment"
    return adj, explain