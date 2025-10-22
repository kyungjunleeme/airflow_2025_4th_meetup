from src.airflow_compat_demo.defaults import DefaultResolver

def test_default_precedence():
    resolver = DefaultResolver(
        schema_defaults={"retries": 1, "owner": "airflow"},
        client_defaults={"owner": "sdk_client"},
        dag_defaults={"retries": 2},
        partial_args={"owner": "dag_owner"},
    )
    # task provides no explicit overrides
    final = resolver.resolve(task_values={"task_id": "x"})
    # owner should be from partial > dag > client > schema => dag_owner
    assert final["owner"] == "dag_owner"
    # retries should be from dag_defaults (2)
    assert final["retries"] == 2
