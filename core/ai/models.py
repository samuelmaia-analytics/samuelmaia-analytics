from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class GenAIContext:
    projects: list[dict[str, Any]]
    quality_report: dict[str, Any]
    semantic_metrics: dict[str, float]
    metric_catalog: dict[str, Any]
    repository_registry: list[dict[str, Any]]
    operational_context: dict[str, Any]


@dataclass(frozen=True)
class GenAITaskRequest:
    use_case: str
    prompt_name: str
    title: str
    focus: str
    context: GenAIContext
    parameters: dict[str, Any]


@dataclass(frozen=True)
class GenAIArtifact:
    use_case: str
    title: str
    narrative: str
    bullets: list[str]
    provider_status: str
    provider_name: str
    model: str
    prompt_reference: str
    generation_mode: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
