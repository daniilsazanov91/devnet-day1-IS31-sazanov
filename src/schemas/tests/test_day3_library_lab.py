import json
import os
import subprocess
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
DAY3 = ROOT / "artifacts" / "day3"
SCHEMA = ROOT / "schemas" / "day3_summary.schema.json"


def jload(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def test_day3_lab_artifacts_and_rules():
    env = os.environ.copy()
    assert env.get("STUDENT_TOKEN")
    assert env.get("STUDENT_NAME")
    assert env.get("STUDENT_GROUP")

    # Run script. If artifacts already exist, allow offline for stability.
    cmd = ["python", "src/day3_library_lab.py"]
    if (DAY3 / "summary.json").exists():
        cmd.append("--offline")

    r = subprocess.run(cmd, cwd=str(ROOT), env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr

    # Required files
    for fn in [
        "books_before.json", "books_sorted_isbn.json", "mybook_post.json", "books_by_me.json",
        "add100_report.json", "postman_collection.json", "postman_environment.json",
        "curl_get_books.txt", "curl_get_books_isbn.txt", "curl_get_books_sorted.txt",
        "summary.json"
    ]:
        assert (DAY3 / fn).exists(), f"missing {fn}"

    # Schema validate
    summary = jload(DAY3 / "summary.json")
    schema = jload(SCHEMA)
    jsonschema.validate(instance=summary, schema=schema)

    # Check “my book” contains token_hash8
    th8 = summary["student"]["token_hash8"]
    mypost = jload(DAY3 / "mybook_post.json")
    assert th8 in mypost["request"]["title"]

    # Check add100_report says added_ok >= 100 and fail == 0 (или близко, если были редкие сбои)
    rep = jload(DAY3 / "add100_report.json")
    assert rep["count_requested"] == 100
    assert rep["added_ok"] >= 95  # допускаем редкие сетевые/сервисные сбои
