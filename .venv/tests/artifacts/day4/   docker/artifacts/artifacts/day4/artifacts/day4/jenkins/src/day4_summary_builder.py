#!/usr/bin/env python3
import hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

ART = Path("artifacts/day4")
SCHEMA_VERSION = "4.1"

def now_utc(): return datetime.now(timezone.utc).isoformat()
def sha256_text(s: str): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def sha256_file(p: Path) -> str:
    if not p.exists(): return ""
    return sha256_text(p.read_text(encoding="utf-8", errors="replace"))

def token_hash8(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

def contains(p: Path, needle: str) -> bool:
    return needle in read(p)

def main() -> int:
    token = os.getenv("STUDENT_TOKEN", "").strip()
    name = os.getenv("STUDENT_NAME", "").strip()
    group = os.getenv("STUDENT_GROUP", "").strip()
    th8 = token_hash8(token) if token else ""

    # Paths
    p_docker = ART / "docker" / "sampleapp_curl.txt"
    p_tokenproof = ART / "docker" / "sampleapp_token_proof.txt"
    p_ports = ART / "ansible" / "ports_conf_after.txt"
    p_pipe = ART / "jenkins" / "pipeline_console.txt"
    p_db_tables = ART / "security" / "db_tables.txt"

    # Minimal validations (string markers)
    docker_ok = (th8 != "") and contains(p_docker, "TOKEN_HASH8=") and contains(p_docker, th8)
    tokenproof_ok = contains(p_tokenproof, th8)
    ansible_ok = contains(p_ports, "Listen 8081")
    jenkins_ok = contains(p_pipe, "Preparation") and contains(p_pipe, "Build") and contains(p_pipe, "Results")
    security_ok = contains(p_db_tables, "USER_")  # мягко, чтобы не упираться в формат

    summary = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": now_utc(),
        "student": {"token": token, "token_hash8": th8, "name": name, "group": group},
        "checks": {
            "docker_token_in_page": docker_ok,
            "docker_tokenproof": tokenproof_ok,
            "ansible_port_8081": ansible_ok,
            "jenkins_pipeline_has_stages": jenkins_ok,
            "security_db_has_tables": security_ok,
        },
        "evidence_sha256": {
            # docker
            "docker_sampleapp_curl": sha256_file(ART/"docker"/"sampleapp_curl.txt"),
            "docker_ps": sha256_file(ART/"docker"/"sampleapp_docker_ps.txt"),
            "docker_build_log": sha256_file(ART/"docker"/"sampleapp_build_log.txt"),
            "docker_token_proof": sha256_file(ART/"docker"/"sampleapp_token_proof.txt"),
            # jenkins
            "jenkins_docker_ps": sha256_file(ART/"jenkins"/"jenkins_docker_ps.txt"),
            "buildapp_console": sha256_file(ART/"jenkins"/"buildapp_console.txt"),
            "testapp_console": sha256_file(ART/"jenkins"/"testapp_console.txt"),
            "pipeline_script": sha256_file(ART/"jenkins"/"pipeline_script.groovy"),
            "pipeline_console": sha256_file(ART/"jenkins"/"pipeline_console.txt"),
            "jenkins_url": sha256_file(ART/"jenkins"/"jenkins_url.txt"),
            # ansible
            "ansible_ping": sha256_file(ART/"ansible"/"ansible_ping.txt"),
            "ansible_hello": sha256_file(ART/"ansible"/"ansible_hello.txt"),
            "ansible_playbook_install": sha256_file(ART/"ansible"/"ansible_playbook_install.txt"),
            "ports_conf_after": sha256_file(ART/"ansible"/"ports_conf_after.txt"),
            "curl_apache_8081": sha256_file(ART/"ansible"/"curl_apache_8081.txt"),
            # security
            "signup_v1": sha256_file(ART/"security"/"signup_v1.txt"),
            "login_v1": sha256_file(ART/"security"/"login_v1.txt"),
            "signup_v2": sha256_file(ART/"security"/"signup_v2.txt"),
            "login_v2": sha256_file(ART/"security"/"login_v2.txt"),
            "db_tables": sha256_file(ART/"security"/"db_tables.txt"),
            "db_user_hash_sample": sha256_file(ART/"security"/"db_user_hash_sample.txt"),
        },
        "validation_passed": bool(docker_ok and ansible_ok and jenkins_ok and security_ok),
        "run": {"python": sys.version.split()[0], "platform": sys.platform},
    }

    out = ART / "summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["validation_passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
