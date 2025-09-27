import os, re, tempfile
from collections import defaultdict
import nbformat
from github import Github
from git import Repo
from .config import GITHUB_TOKEN, MAX_REPOS, BASE_SKILL_LEXICON
from .utils import normalize_token, IMPORT_RE

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

            # Languages
            for lang in repo.get_languages().keys():
                skills_found[normalize_token(lang)].append(dict(
                    source="github", repo=name, type="language", detail=lang, loc=loc, recency=pushed
                ))

            # Dependency files
            try:
                contents = repo.get_contents("")
                topnames = {c.name.lower(): c for c in contents}
            except Exception:
                topnames = {}

            for fname in ("requirements.txt","pyproject.toml","package.json","Pipfile","environment.yml"):
                if fname in topnames:
                    try:
                        body = repo.get_contents(fname).decoded_content.decode('utf-8', errors='ignore')
                        for tok in re.findall(r'[A-Za-z0-9_\-\.]+', body):
                            skills_found[normalize_token(tok)].append(dict(
                                source="github", repo=name, type="dependency_file",
                                detail=tok, file=fname, loc=loc, recency=pushed
                            ))
                    except Exception:
                        pass

            # Shallow clone for imports
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
                                                skills_found[normalize_token(base)].append(dict(
                                                    source="github", repo=name, type="import",
                                                    detail=token, file=f, loc=loc, recency=pushed
                                                ))
                                except Exception:
                                    pass
                except Exception:
                    pass

            # README scan
            for tok in BASE_SKILL_LEXICON.keys():
                if re.search(r'\b'+re.escape(tok)+r'\b', readme_text, re.I):
                    skills_found[normalize_token(tok)].append(dict(
                        source="github", repo=name, type="readme",
                        detail=tok, loc=loc, recency=pushed
                    ))
        except Exception:
            pass

    return skills_found
