from __future__ import annotations

import json
from dataclasses import dataclass
from urllib import error, request

from core.ai.models import GenAITaskRequest


@dataclass(frozen=True)
class ProviderResult:
    narrative: str
    bullets: list[str]
    provider_status: str
    generation_mode: str


class GenAIProvider:
    provider_name: str

    def generate(self, task: GenAITaskRequest, prompt_text: str, fallback: ProviderResult) -> ProviderResult:
        raise NotImplementedError


class TemplateGenAIProvider(GenAIProvider):
    provider_name = "local-template"

    def generate(self, task: GenAITaskRequest, prompt_text: str, fallback: ProviderResult) -> ProviderResult:
        return fallback


class OpenAICompatibleGenAIProvider(GenAIProvider):
    provider_name = "openai-compatible"

    def __init__(
        self,
        model: str,
        base_url: str,
        api_key: str,
        timeout_seconds: int,
        max_retries: int,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries

    def generate(self, task: GenAITaskRequest, prompt_text: str, fallback: ProviderResult) -> ProviderResult:
        if not self.base_url or not self.api_key:
            return ProviderResult(
                narrative=fallback.narrative,
                bullets=fallback.bullets,
                provider_status="remote_fallback",
                generation_mode=fallback.generation_mode,
            )

        try:
            remote = self._call_remote(task, prompt_text)
        except (error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError):
            return ProviderResult(
                narrative=fallback.narrative,
                bullets=fallback.bullets,
                provider_status="remote_fallback",
                generation_mode=fallback.generation_mode,
            )

        return ProviderResult(
            narrative=remote["narrative"],
            bullets=remote["bullets"],
            provider_status="remote_ok",
            generation_mode="llm",
        )

    def _call_remote(self, task: GenAITaskRequest, prompt_text: str) -> dict[str, object]:
        url = self.base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": prompt_text},
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "use_case": task.use_case,
                            "title": task.title,
                            "focus": task.focus,
                            "parameters": task.parameters,
                            "context": {
                                "projects": task.context.projects,
                                "quality_report": task.context.quality_report,
                                "semantic_metrics": task.context.semantic_metrics,
                                "metric_catalog": task.context.metric_catalog,
                                "repository_registry": task.context.repository_registry,
                            },
                            "required_output": {
                                "narrative": "string",
                                "bullets": ["string", "string", "string"],
                            },
                        }
                    ),
                },
            ],
            "temperature": 0.2,
        }
        req = request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        last_error: Exception | None = None
        for _attempt in range(self.max_retries + 1):
            try:
                with request.urlopen(req, timeout=self.timeout_seconds) as response:
                    body = json.loads(response.read().decode("utf-8"))
                content = body["choices"][0]["message"]["content"].strip()
                parsed = json.loads(content)
                return {
                    "narrative": str(parsed["narrative"]).strip(),
                    "bullets": [str(item).strip() for item in parsed["bullets"]][:3],
                }
            except (error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as exc:
                last_error = exc
        assert last_error is not None
        raise last_error
