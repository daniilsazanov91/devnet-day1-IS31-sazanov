import os
import json
import hashlib
from pathlib import Path

ART = Path("artifacts/day5")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def token_hash8():
    token = os.getenv("STUDENT_TOKEN", "")
    return hashlib.sha256(token.encode()).hexdigest()[:8]


def read_json(path):
    with open(path) as f:
        return json.load(f)


def check_yang():
    tree_file = ART / "yang/pyang_tree.txt"

    if not tree_file.exists():
        return False, None

    content = tree_file.read_text()

    ok = "+--rw interfaces" in content

    return ok, sha256_file(tree_file)


def check_webex():
    file = ART / "webex/room_create.json"

    if not file.exists():
        return False, False, None

    data = read_json(file)

    title = data.get("title", "")

    h = token_hash8()

    return h in title, h in title, sha256_file(file)


def check_pt():
    check_file = ART / "pt/external_access_check.json"
    dev_file = ART / "pt/network_devices.json"
    host_file = ART / "pt/hosts.json"

    if not check_file.exists():
        return False, False, None

    text = check_file.read_text()

    empty_ticket = "empty ticket" in text.lower()

    version_ok = False

    if dev_file.exists() and host_file.exists():
        dev = read_json(dev_file)
        host = read_json(host_file)

        version_ok = (
            dev.get("version") == "1.0"
            and host.get("version") == "1.0"
        )

    ok = empty_ticket and version_ok

    return ok, empty_ticket, sha256_file(check_file)


def build_summary():

    student = {
        "token": os.getenv("STUDENT_TOKEN"),
        "token_hash8": token_hash8(),
        "name": os.getenv("STUDENT_NAME"),
        "group": os.getenv("STUDENT_GROUP")
    }

    yang_ok, yang_sha = check_yang()

    webex_ok, room_hash, webex_sha = check_webex()

    pt_ok, empty_ticket, pt_sha = check_pt()

    summary = {
        "schema_version": "5.0",
        "student": student,
        "yang": {
            "ok": yang_ok,
            "evidence_sha": yang_sha
        },
        "webex": {
            "ok": webex_ok,
            "room_title_contains_hash8": room_hash,
            "evidence_sha": webex_sha
        },
        "pt": {
            "ok": pt_ok,
            "empty_ticket_seen": empty_ticket,
            "evidence_sha": pt_sha
        },
        "validation_passed": all([yang_ok, webex_ok, pt_ok])
    }

    out = ART / "summary.json"

    out.write_text(json.dumps(summary, indent=2))

    return summary


if __name__ == "__main__":
    print(json.dumps(build_summary(), indent=2))
