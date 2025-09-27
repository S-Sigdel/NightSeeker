#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv || true
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

export PYTHONPATH="$(pwd)"${PYTHONPATH:+":$PYTHONPATH"}

PORT=${PORT:-8001}
exec uvicorn app.main:app --host 127.0.0.1 --port "$PORT" --reload

