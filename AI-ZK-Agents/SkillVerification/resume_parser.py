import io, re
import pdfplumber
from .utils import normalize_token, normalize_to_lexicon
from .config import BASE_SKILL_LEXICON

def parse_resume_pdf_bytes(pdf_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for p in pdf.pages:
            text += p.extract_text() or ""
            text += "\n"
    return text

def extract_skills_from_resume_text(text):
    skills = []
    lower = text.lower()
    m = re.search(r'(skills|technical skills|technologies|proficiencies)[:\s\-]+\n?(.{10,800})', lower, re.I)
    if m:
        block = m.group(2)
        block = re.split(r'\n[A-Z][a-z]{1,30}[:\n]', block, maxsplit=1)[0]
        tokens = re.split(r'[,\n;/•\u2022]+', block)
        for t in tokens:
            s = re.sub(r'[^a-zA-Z0-9_\-+#\. ]','', t).strip()
            if not s: continue
            canon = normalize_to_lexicon(s)
            if canon:
                skills.append((canon, "resume_skills_section"))

    for token in BASE_SKILL_LEXICON.keys():
        if re.search(r'\b'+re.escape(token)+r'\b', lower):
            skills.append((normalize_token(token), "resume_mention"))

    out, seen = [], set()
    for s,src in skills:
        if s not in seen:
            seen.add(s)
            out.append((s,src))
    return out