import json
import os
import re
from dataclasses import dataclass
from datetime import datetime
from hashlib import blake2b
from typing import Any, Dict, List, Tuple


VERSION = "0.1.0"


def canonical_dumps(obj: Any) -> bytes:
    """Serialize object to canonical JSON bytes (sorted keys, no spaces)."""
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def hash32(payload: bytes) -> bytes:
    h = blake2b(digest_size=32)
    h.update(payload)
    return h.digest()


def derive_secret(domain: str, payload_obj: Any, salt: bytes | None = None) -> bytes:
    domain_prefix = f"MAI-{domain}|".encode("utf-8")
    payload = canonical_dumps(payload_obj)
    if salt:
        return hash32(domain_prefix + salt + b"|" + payload)
    return hash32(domain_prefix + payload)


def commitment_from_secret(secret32: bytes) -> bytes:
    return hash32(b"MAI-COMMIT-v1|" + secret32)


def to_hex32(b: bytes) -> str:
    if len(b) != 32:
        raise ValueError("expected 32-byte value")
    return "0x" + b.hex()


def now_utc_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def is_probable_json(s: str) -> bool:
    s = s.strip()
    return (s.startswith("{") and s.endswith("}")) or (s.startswith("[") and s.endswith("]"))


def load_json_or_path(arg: str) -> Any:
    """Accept either a JSON string or a filesystem path to JSON."""
    if os.path.exists(arg):
        with open(arg, "r", encoding="utf-8") as fh:
            return json.load(fh)
    if is_probable_json(arg):
        return json.loads(arg)
    raise ValueError(f"Argument is neither existing path nor JSON: {arg}")


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


def hex_to_bytes32(x: str) -> bytes:
    x = x.lower().strip()
    if x.startswith("0x"):
        x = x[2:]
    b = bytes.fromhex(x)
    if len(b) != 32:
        raise ValueError("expected 32-byte hex value")
    return b


@dataclass
class MatchResult:
    job_id: str
    candidate_id: str
    score: float
    is_match: bool
    threshold: float
    details: Dict[str, Any]
    job_secret: bytes
    skills_secret: bytes
    match_secret: bytes

    def to_zk_json(self) -> Dict[str, Any]:
        return {
            "module": "MatchingAlgorithm",
            "version": VERSION,
            "generated_at": now_utc_iso(),
            "ids": {"job_id": self.job_id, "candidate_id": self.candidate_id},
            "public": {
                "match_score": round(self.score, 6),
                "threshold": self.threshold,
                "is_match": self.is_match,
                "job_commitment": to_hex32(commitment_from_secret(self.job_secret)),
                "skills_commitment": to_hex32(commitment_from_secret(self.skills_secret)),
                "match_commitment": to_hex32(commitment_from_secret(self.match_secret)),
            },
            "witness": {
                "job_secret": to_hex32(self.job_secret),
                "skills_secret": to_hex32(self.skills_secret),
                "match_secret": to_hex32(self.match_secret),
                "hash_algo": "blake2b-256",
                "domain": "MAI-*-v1",
            },
            "details": self.details,
        }


