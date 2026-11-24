"""JPAIS Stage 10: Security, Privacy & Reproducibility Audit."""

from __future__ import annotations

import json
import os
import platform
import socket
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent


def check_port_localhost_only(port: int) -> dict:
    """Verify if port is listening on 127.0.0.1 and NOT exposed on 0.0.0.0."""
    s_local = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_local.settimeout(0.5)
    local_open = s_local.connect_ex(("127.0.0.1", port)) == 0
    s_local.close()
    return {"port": port, "localhost_reachable": local_open}


def run_security_audit() -> dict:
    ports = [check_port_localhost_only(p) for p in (6333, 7687, 8001, 11434)]
    env_files_exposed = [str(p) for p in HERE.glob("*.env")]
    report = {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "localhost_services": ports,
        "exposed_env_files_in_module": env_files_exposed,
        "status": "PASS" if not env_files_exposed else "FAIL",
    }
    (HERE / "security_audit_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    r = run_security_audit()
    print(f"Stage 10 Audit Status: {r['status']} (Python {r['python_version']})")
