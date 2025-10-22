from __future__ import annotations
from typing import Dict, Any

class DefaultResolver:
    """Applies default precedence:
    1) schema (lowest)
    2) client
    3) dag default_args
    4) partial args (e.g., shared for mapped)
    5) task explicit (highest)
    """

    def __init__(self, schema_defaults: Dict[str, Any], client_defaults: Dict[str, Any],
                 dag_defaults: Dict[str, Any], partial_args: Dict[str, Any]) -> None:
        self.schema_defaults = dict(schema_defaults)
        self.client_defaults = dict(client_defaults)
        self.dag_defaults = dict(dag_defaults)
        self.partial_args = dict(partial_args)

    def resolve(self, task_values: Dict[str, Any]) -> Dict[str, Any]:
        merged: Dict[str, Any] = {}
        merged.update(self.schema_defaults)
        merged.update(self.client_defaults)
        merged.update(self.dag_defaults)
        merged.update(self.partial_args)
        merged.update(task_values)  # explicit wins
        return merged
