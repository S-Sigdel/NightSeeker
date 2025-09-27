from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from SkillVerification.core import run_for_candidate

load_dotenv()
app = Flask(__name__)


@app.get("/")
def index():
    return """
    <form method="post" enctype="multipart/form-data" action="/upload">
      <input type="text" name="candidate_id" placeholder="candidate-123" />
      <input type="file" name="resume" accept="application/pdf" />
      <button type="submit">Upload</button>
    </form>
    """


@app.post("/upload")
def upload():
    file = request.files.get("resume")
    candidate_id = request.form.get("candidate_id", "web-upload")
    if not file or file.filename == "":
        return jsonify({"error": "resume file required"}), 400

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        file.save(tmp.name)
        temp_path = Path(tmp.name)

    try:
        result = run_for_candidate(candidate_id=candidate_id, resume_paths=[str(temp_path)])
        return jsonify(result)
    finally:
        temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)