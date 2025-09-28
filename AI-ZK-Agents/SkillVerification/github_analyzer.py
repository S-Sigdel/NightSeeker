import os, re, tempfile, json
from collections import defaultdict
import nbformat
from github import Github
from git import Repo
from .config import GITHUB_TOKEN, MAX_REPOS, BASE_SKILL_LEXICON
from .utils import normalize_to_lexicon, IMPORT_RE

def _iter_dep_tokens_from_text(fname, body):
    if fname == "package.json":
        try:
            data = json.loads(body)
        except Exception:
            return []
        names = set()
        for k in ("dependencies","devDependencies","peerDependencies","optionalDependencies"):
            d = data.get(k, {})
            if isinstance(d, dict):
                names.update(d.keys())
        return list(names)
    if fname == "requirements.txt":
        toks = []
        for line in body.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            name = re.split(r'[<>=!~\[\];\s]', s)[0]
            if name:
                toks.append(name)
        return toks
    # fallback: scan tokens but drop pure versions/numbers and common keys
    bad_keys = {"name","version","license","author","keywords","description","scripts","main","type"}
    toks = []
    for tok in re.findall(r'[A-Za-z0-9_\-\.]+', body):
        if re.fullmatch(r'\d+(?:\.\d+)*', tok):
            continue
        if tok.lower() in bad_keys:
            continue
        toks.append(tok)
    return toks

def analyze_github_user(username, max_repos=MAX_REPOS):
    gh = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()
    user = gh.get_user(username)
    repos = list(user.get_repos())[:max_repos]
    skills_found = defaultdict(list)

    for repo in repos:
        try:
            name = repo.full_name
            pushed = repo.pushed_at
            loc = max(10, repo.size * 50)  # rough LOC estimate
            readme_text = ""

            try:
                readme_text = repo.get_readme().decoded_content.decode('utf-8', errors='ignore')
            except Exception:
                pass

            # Languages → keep only lexicon skills
            try:
                for lang in repo.get_languages().keys():
                    canon = normalize_to_lexicon(lang)
                    if canon:
                        skills_found[canon].append(dict(
                            source="github", repo=name, type="language", detail=lang, loc=loc, recency=pushed
                        ))
            except Exception:
                pass

            # Dependency files → parse and keep only lexicon skills
            try:
                contents = repo.get_contents("")
                topnames = {c.name.lower(): c for c in contents}
            except Exception:
                topnames = {}

            for fname in ("requirements.txt","pyproject.toml","package.json","Pipfile","environment.yml"):
                if fname in topnames:
                    try:
                        body = repo.get_contents(fname).decoded_content.decode('utf-8', errors='ignore')
                        for tok in _iter_dep_tokens_from_text(fname, body):
                            canon = normalize_to_lexicon(tok)
                            if not canon:
                                continue
                            skills_found[canon].append(dict(
                                source="github", repo=name, type="dependency_file",
                                detail=tok, file=fname, loc=loc, recency=pushed
                            ))
                    except Exception:
                        pass

            # Shallow clone for imports → keep only lexicon skills
            if repo.size < 2000:
                tmp = tempfile.mkdtemp(prefix="repo_")
                giturl = repo.clone_url
                if GITHUB_TOKEN:
                    giturl = giturl.replace("https://", f"https://{GITHUB_TOKEN}@")
                try:
                    Repo.clone_from(giturl, tmp, depth=1)
                    for root, _, files in os.walk(tmp):
                        for f in files:
                            if f.endswith(('.py','.ipynb','.js','.ts')):
                                fp = os.path.join(root, f)
                                try:
                                    with open(fp,'r',errors='ignore') as fh:
                                        data = fh.read()
                                        if f.endswith('.ipynb'):
                                            nb = nbformat.reads(data, as_version=4)
                                            data = "\n".join(cell.source for cell in nb.cells if cell.cell_type == 'code')
                                        for m in IMPORT_RE.finditer(data):
                                            token = m.group(1) or m.group(2)
                                            if token:
                                                base = token.split('.')[0]
                                                canon = normalize_to_lexicon(base)
                                                if not canon:
                                                    continue
                                                skills_found[canon].append(dict(
                                                    source="github", repo=name, type="import",
                                                    detail=token, file=f, loc=loc, recency=pushed
                                                ))
                                except Exception:
                                    pass
                except Exception:
                    pass

            # README scan → lexicon tokens only
            for tok in BASE_SKILL_LEXICON.keys():
                try:
                    if re.search(r'\b'+re.escape(tok)+r'\b', readme_text, re.I):
                        canon = normalize_to_lexicon(tok)
                        if canon:
                            skills_found[canon].append(dict(
                                source="github", repo=name, type="readme",
                                detail=tok, loc=loc, recency=pushed
                            ))
                except Exception:
                    pass
        except Exception:
            pass

    return skills_found