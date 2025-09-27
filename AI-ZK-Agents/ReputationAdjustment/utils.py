import json
from dataclasses import dataclass
from datetime import datetime
from hashlib import blake2b
from typing import Any, Dict


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
    domain_prefix = f"RA-{domain}|".encode("utf-8")
    payload = canonical_dumps(payload_obj)
    if salt:
        return hash32(domain_prefix + salt + b"|" + payload)
    return hash32(domain_prefix + payload)


def commitment_from_secret(secret32: bytes) -> bytes:
    return hash32(b"RA-COMMIT-v1|" + secret32)


@dataclass
class ReputationResult:
    worker_id: str
    base_reputation: float
    job_complexity: float
    employer_rating: float
    verified_projects: int
    new_reputation: float
    details: Dict[str, Any]
    worker_secret: bytes
    adjustment_secret: bytes

    def to_zk_json(self) -> Dict[str, Any]:
        return {
            "module": "RepurationAdjustment",
            "version": VERSION,
            "generated_at": now_utc_iso(),
            "ids": {"worker_id": self.worker_id},
            "public": {
                "new_reputation": round(self.new_reputation, 6),
                "worker_commitment": to_hex32(commitment_from_secret(self.worker_secret)),
                "adjustment_commitment": to_hex32(commitment_from_secret(self.adjustment_secret)),
            },
            "witness": {
                "worker_secret": to_hex32(self.worker_secret),
                "adjustment_secret": to_hex32(self.adjustment_secret),
                "hash_algo": "blake2b-256",
                "domain": "RA-*-v1",
            },
            "details": self.details,
        }


