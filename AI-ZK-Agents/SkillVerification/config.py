import os
import math

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY environment variable before running.")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # optional

MAX_REPOS = 12
WEIGHTS = {"repo": 0.6, "notebook": 0.25, "resume": 0.15}
MAX_EXPECTED = math.log(250)

EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

BASE_SKILL_LEXICON = {
    "python": "Python", "javascript": "JavaScript", "ts": "TypeScript", "numpy": "NumPy",
    "pandas": "Pandas", "sklearn": "Scikit-Learn", "scikit-learn": "Scikit-Learn",
    "tensorflow": "TensorFlow", "torch": "PyTorch", "keras": "Keras",
    "docker": "Docker", "kubernetes": "Kubernetes", "aws": "AWS", "azure": "Azure", "gcp": "GCP",
    "react": "React", "django": "Django", "flask": "Flask",
}
