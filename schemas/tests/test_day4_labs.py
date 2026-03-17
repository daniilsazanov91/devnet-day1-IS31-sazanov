import json, os, subprocess
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "day4"
SCHEMA = ROOT / "schemas" / "day4_summary.schema.json"

def jload(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def test_day4_summary_and_required_evidence():
    env = os.environ.copy()
    assert env.get("STUDENT_TOKEN")
    assert env.get("STUDENT_NAME")
    assert env.get("STUDENT_GROUP")

    r = subprocess.run(["python", "src/day4_summary_builder.py"], cwd=str(ROOT), env=env, capture_output=True, text=True)
    assert r.returncode in (0, 2), r.stderr

    assert (ART / "summary.json").exists()
    summary = jload(ART / "summary.json")
    schema = jload(SCHEMA)
    jsonschema.validate(instance=summary, schema=schema)

    # сильные проверки
    assert summary["checks"]["docker_token_in_page"] is True
    assert summary["checks"]["ansible_port_8081"] is True
    assert summary["checks"]["jenkins_pipeline_has_stages"] is True
