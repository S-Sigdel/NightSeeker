import json
import os
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from hashlib import blake2b
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


VERSION = "0.1.0"


def canonical_dumps(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def hash32(payload: bytes) -> bytes:
    h = blake2b(digest_size=32)
    h.update(payload)
    return h.digest()


def to_hex32(b: bytes) -> str:
    if len(b) != 32:
        raise ValueError("expected 32-byte value")
    return "0x" + b.hex()


def now_utc_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def derive_secret(domain: str, payload_obj: Any, salt: bytes | None = None) -> bytes:
    domain_prefix = f"PV-{domain}|".encode("utf-8")
    payload = canonical_dumps(payload_obj)
    if salt:
        return hash32(domain_prefix + salt + b"|" + payload)
    return hash32(domain_prefix + payload)


def commitment_from_secret(secret32: bytes) -> bytes:
    return hash32(b"PV-COMMIT-v1|" + secret32)


def git_describe(path: str) -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=path, stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return ""


def list_repo_files(path: str) -> List[str]:
    files = []
    for root, _, filenames in os.walk(path):
        for fn in filenames:
            p = os.path.join(root, fn)
            files.append(os.path.relpath(p, path))
    return sorted(files)


def read_text_safe(path: str, max_bytes: int = 200_000) -> str:
    try:
        with open(path, "rb") as fh:
            data = fh.read(max_bytes)
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return ""


def normalize_skill_name(name: str) -> str:
    t = name.strip().lower()
    t = re.sub(r"[^a-z0-9_\-+.#]", "", t)
    aliases = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "sklearn": "scikit-learn",
        "tf": "tensorflow",
        "torch": "pytorch",
    }
    t = aliases.get(t, t)
    return t


def score_repo_against_requirements(repo_path: str, requirements: Dict[str, float]) -> Tuple[float, Dict[str, Any]]:
    """Heuristic: detect skills via filename/content keywords and compute overlap.

    requirements: normalized skill -> weight [0,1]
    Returns (coverage_score, details)
    """
    repo_abs = os.path.abspath(repo_path)
    file_list = list_repo_files(repo_abs)
    detected: Dict[str, float] = {}

    keywords = {
        "python": [".py", "python"],
        "javascript": [".js", "javascript"],
        "typescript": [".ts", "typescript"],
        "docker": ["dockerfile", "docker-compose", "FROM "],
        "kubernetes": ["k8s", "apiVersion:", "kind:"],
        "pandas": ["import pandas", "read_csv("],
        "numpy": ["import numpy", "np."],
        "pytorch": ["import torch", "torch."],
        "tensorflow": ["import tensorflow", "tf."],
    }

    # Simple heuristic: any match gives confidence 1.0 for that skill
    for rel in file_list:
        lower = rel.lower()
        abspath = os.path.join(repo_abs, rel)
        text = read_text_safe(abspath)
        for skill, cues in keywords.items():
            if any(cue.lower() in lower for cue in cues) or any(cue.lower() in text.lower() for cue in cues):
                detected[skill] = max(1.0, detected.get(skill, 0.0))

    # Compute coverage against requirements
    req = {normalize_skill_name(k): max(0.0, min(1.0, float(v))) for k, v in requirements.items()}
    denom = sum(req.values()) or 1.0
    overlap = 0.0
    per_skill: List[Dict[str, Any]] = []
    for s, w in req.items():
        conf = 1.0 if detected.get(s) else 0.0
        contrib = min(w, conf)
        overlap += contrib
        per_skill.append({
            "skill": s,
            "required_weight": round(w, 6),
            "detected": bool(detected.get(s)),
            "contribution": round(contrib, 6),
        })

    coverage = overlap / denom
    details = {
        "repo": {
            "path": repo_abs,
            "git_head": git_describe(repo_abs),
            "files": file_list,
        },
        "requirements": req,
        "detected_skills": sorted(list(detected.keys())),
        "per_skill": per_skill,
        "overlap_sum": round(overlap, 6),
        "denominator": round(denom, 6),
    }
    return coverage, details


@dataclass
class VerificationResult:
    job_id: str
    submission_id: str
    worker_id: str
    coverage: float
    passed: bool
    threshold: float
    details: Dict[str, Any]
    job_secret: bytes
    submission_secret: bytes
    nullifier_secret: bytes

    def to_zk_json(self) -> Dict[str, Any]:
        return {
            "module": "ProjectVerification",
            "version": VERSION,
            "generated_at": now_utc_iso(),
            "ids": {"job_id": self.job_id, "submission_id": self.submission_id, "worker_id": self.worker_id},
            "public": {
                "coverage": round(self.coverage, 6),
                "threshold": self.threshold,
                "passed": self.passed,
                "job_commitment": to_hex32(commitment_from_secret(self.job_secret)),
                "submission_commitment": to_hex32(commitment_from_secret(self.submission_secret)),
                "release_nullifier": to_hex32(self.nullifier_secret),
            },
            "witness": {
                "job_secret": to_hex32(self.job_secret),
                "submission_secret": to_hex32(self.submission_secret),
                "nullifier_secret": to_hex32(self.nullifier_secret),
                "hash_algo": "blake2b-256",
                "domain": "PV-*-v1",
            },
            "details": self.details,
        }


