from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Any, Tuple

@dataclass
class VersionChange:
    """Represents a change between two model versions.
    When migrating from `from_version` -> `to_version`, `apply(payload)` is executed.
    """
    from_version: str
    to_version: str
    description: str
    apply: Callable[[Dict[str, Any]], Dict[str, Any]]

class VersionRegistry:
    def __init__(self) -> None:
        self._changes: Dict[Tuple[str, str], VersionChange] = {}

    def register(self, change: VersionChange) -> None:
        key = (change.from_version, change.to_version)
        if key in self._changes:
            raise ValueError(f"Duplicate change for {key}")
        self._changes[key] = change

    def migrate(self, payload: Dict[str, Any], from_version: str, to_version: str) -> Dict[str, Any]:
        if from_version == to_version:
            return payload
        key = (from_version, to_version)
        if key not in self._changes:
            raise ValueError(f"No migration rule from {from_version} to {to_version}")
        change = self._changes[key]
        return change.apply(payload)

# A tiny global registry for the demo
registry = VersionRegistry()

def _remove_dag_version_id(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload = dict(payload)
    payload.pop("dag_version_id", None)
    return payload

# Register: server v1.1 -> client v1.0
registry.register(
    VersionChange(
        from_version="1.1",
        to_version="1.0",
        description="Remove dag_version_id for backward compatibility",
        apply=_remove_dag_version_id,
    )
)
