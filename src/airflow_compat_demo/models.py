from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

@dataclass
class TaskInstanceV11:
    task_id: str
    retries: int = 3           # schema default
    owner: str = "airflow"     # schema default
    dag_version_id: Optional[int] = None  # added in v1.1

@dataclass
class TaskInstanceV10:
    task_id: str
    retries: int = 3
    owner: str = "airflow"
