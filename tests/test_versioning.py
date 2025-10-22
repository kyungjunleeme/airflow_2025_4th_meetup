from src.airflow_compat_demo.versioning import registry

def test_backward_migration_removes_dag_version_id():
    # server v1.1 payload
    payload = {"task_id": "t1", "retries": 3, "owner": "airflow", "dag_version_id": 99}
    out = registry.migrate(payload, from_version="1.1", to_version="1.0")
    assert "dag_version_id" not in out
    assert out["task_id"] == "t1"
