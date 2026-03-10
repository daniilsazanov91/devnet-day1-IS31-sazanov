import json
import os
import subprocess
from pathlib import Path

import os, json, subprocess, jsonschema
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART_DIR = ROOT / "artifacts" / "day1"
SUMMARY = ART_DIR / "summary.json"
SCHEMA = ROOT / "schemas" / "day1_summary.schema.json"

def test_day1_artifacts_and_schema():
    cmd = ["python", "src/day1_api_hello.py"]
    if (ART_DIR / "response.json").exists():
        cmd.append("--offline")

    env = os.environ.copy()
    assert env.get("STUDENT_TOKEN")
    assert env.get("STUDENT_NAME")
    assert env.get("STUDENT_GROUP")

    r = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
    assert r.returncode in (0,2)
    assert SUMMARY.exists()
    assert SCHEMA.exists()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    jsonschema.validate(instance=summary, schema=schema)
             assert isinstance(summary["api"]
             ["validation_passed"], bool)
