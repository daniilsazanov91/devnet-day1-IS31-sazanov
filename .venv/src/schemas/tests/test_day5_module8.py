import json
import os
import hashlib
from pathlib import Path
import jsonschema

ART = Path("artifacts/day5")


def test_summary_exists():
    assert (ART / "summary.json").exists()


def test_schema_validation():

    summary = json.loads((ART / "summary.json").read_text())

    schema = json.loads(
        Path("schemas/day5_summary.schema.json").read_text()
    )

    jsonschema.validate(summary, schema)


def test_token_hash():

    summary = json.loads((ART / "summary.json").read_text())

    token = os.getenv("STUDENT_TOKEN", "")

    expected = hashlib.sha256(token.encode()).hexdigest()[:8]

    assert summary["student"]["token_hash8"] == expected


def test_artifacts_exist():

    required = [
        "yang/ietf-interfaces.yang",
        "yang/pyang_tree.txt",
        "webex/room_create.json",
        "pt/external_access_check.json"
    ]

    for r in required:
        assert (ART / r).exists()


def test_validation_passed():

    summary = json.loads((ART / "summary.json").read_text())

    assert summary["validation_passed"] is True
