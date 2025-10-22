from __future__ import annotations
from dataclasses import asdict
from typing import Dict, Any

from .models import TaskInstanceV11
from .versioning import registry
from .defaults import DefaultResolver

def simulate_request(client_version: str = "1.0", server_version: str = "1.1") -> Dict[str, Any]:
    # Server creates the latest model (v1.1) with a new field
    ti = TaskInstanceV11(task_id="transform_users", dag_version_id=101)
    raw = asdict(ti)

    # Apply backward migration if needed
    migrated = registry.migrate(raw, from_version=server_version, to_version=client_version)

    # Apply default precedence resolution
    resolver = DefaultResolver(
        schema_defaults={"retries": 1, "owner": "airflow"},
        client_defaults={"owner": "sdk_client"},
        dag_defaults={"retries": 2},
        partial_args={"owner": "dag_owner"},
    )
    final = resolver.resolve(task_values=migrated)
    return final

def main() -> None:
    res = simulate_request(client_version="1.0", server_version="1.1")
    print("[Response for SDK v1.0]", res)
    res_same = simulate_request(client_version="1.1", server_version="1.1")
    print("[Response for SDK v1.1]", res_same)
