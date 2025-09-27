import re
from datetime import datetime
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

def months_since(dt):
    if not dt: return 999
    if isinstance(dt, datetime):
        delta = datetime.utcnow() - dt
    else:
        try:
            delta = datetime.utcnow() - datetime.fromtimestamp(dt)
        except Exception:
            return 999
    return delta.days / 30.0
