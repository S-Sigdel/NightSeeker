import requests
from collections import defaultdict
from .utils import normalize_to_lexicon, IMPORT_RE

def analyze_kaggle_notebook(url):
    skills = defaultdict(list)
    try:
        r = requests.get(url, timeout=10)
        text = r.text
        for m in IMPORT_RE.finditer(text):
            tok = (m.group(1) or m.group(2)).split('.')[0]
            canon = normalize_to_lexicon(tok)
            if canon:
                skills[canon].append(dict(
                    source="kaggle", url=url, type="import", detail=tok
                ))
    except Exception:
        pass
    return skills