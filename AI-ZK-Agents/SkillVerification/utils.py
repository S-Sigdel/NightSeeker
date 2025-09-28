import re
from datetime import datetime, timezone
from .config import BASE_SKILL_LEXICON

IMPORT_RE = re.compile(
    r'^\s*(?:from\s+([A-Za-z0-9_\.]+)\s+import|import\s+([A-Za-z0-9_\.]+))',
    re.MULTILINE
)

def normalize_token(token):
    t = token.strip().lower()
    t = re.sub(r'[^a-z0-9_\-+.#]', '', t)
    if t in BASE_SKILL_LEXICON:
        return BASE_SKILL_LEXICON[t]
    t = re.sub(r'([=<>!].*)$', '', t)
    if t in BASE_SKILL_LEXICON:
        return BASE_SKILL_LEXICON[t]
    return token.capitalize()

def normalize_to_lexicon(token):
    t = (token or "").strip()
    if not t:
        return None
    t_low = re.sub(r'[^A-Za-z0-9_\-+.#]', '', t).lower()
    if t_low in BASE_SKILL_LEXICON:
        return BASE_SKILL_LEXICON[t_low]
    for canon in BASE_SKILL_LEXICON.values():
        if canon.lower() == t_low:
            return canon
    return None

def is_skill_token(token):
    return normalize_to_lexicon(token) is not None

def months_since(dt):
    if not dt: return 999
    try:
        if isinstance(dt, datetime):
            d = dt
        else:
            d = datetime.fromtimestamp(float(dt), tz=timezone.utc)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = now - d.astimezone(timezone.utc)
        return delta.days / 30.0
    except Exception:
        return 999