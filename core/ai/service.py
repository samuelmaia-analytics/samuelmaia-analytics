from __future__ import annotations

from typing import Any

from config.settings import Settings
from core.ai.models import GenAIArtifact, GenAIContext, GenAITaskRequest
from core.ai.providers import OpenAICompatibleGenAIProvider, ProviderResult, TemplateGenAIProvider


class AnalyticsGenAIService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.prompt_dir = settings.genai_prompt_dir
        self.provider = self._build_provider()

    def build_suite(
        self,
        context: GenAIContext,
        metric_name: str | None = None,
        glossary_term: str | None = None,
        dataset_name: str | None = None,
    ) -> dict[str, dict[str, Any]]:
        metric_name = metric_name or self._select_primary_metric(context)
        glossary_term = glossary_term or metric_name
        dataset_name = dataset_name or "portfolio_snapshot"

        outputs = {
            "narrative_kpi_insights": self.narrative_kpi_insights(context),
            "executive_summary": self.executive_summary(context),
            "anomaly_explanation_draft": self.anomaly_explanation_draft(context),
            "metric_definition_assistant": self.metric_definition_assistant(context, metric_name),
            "business_glossary_explanation": self.business_glossary_explanation(context, glossary_term),
            "pipeline_dataset_description": self.pipeline_dataset_description(context, dataset_name),
        }
        return {name: artifact.to_dict() for name, artifact in outputs.items()}

    def narrative_kpi_insights(self, context: GenAIContext) -> GenAIArtifact:
        semantic_metrics = context.semantic_metrics
        top_metric = max(semantic_metrics.items(), key=lambda item: item[1])
        focus = (
            f"Decision readiness is {semantic_metrics['decision_readiness_score']:.1f}, "
            f"quality pass rate is {semantic_metrics['quality_pass_rate']:.1f}%, and "
            f"trust score is {semantic_metrics['platform_trust_score']:.1f}. "
            f"Run history: {context.operational_context.get('run_history', {}).get('trend_summary', 'no trend data')}."
        )
        bullets = [
            f"Strongest KPI signal: {top_metric[0]} at {top_metric[1]:.1f}.",
            f"Portfolio quality checks passed at {semantic_metrics['quality_pass_rate']:.1f}%.",
            self._project_change_highlight(
                context,
                fallback=context.operational_context.get("snapshot_history", {}).get(
                    "comparison_summary",
                    "Next step: keep converting governed metrics into leader-facing decision surfaces.",
                ),
            ),
        ]
        return self._generate_artifact(
            use_case="narrative_kpi_insights",
            title="Narrative KPI Insights",
            prompt_name="narrative_kpi_insights.md",
            focus=focus,
            context=context,
            parameters={},
            fallback_narrative=(
                f"The KPI surface shows a decision readiness score of "
                f"{semantic_metrics['decision_readiness_score']:.1f}, a quality pass rate of "
                f"{semantic_metrics['quality_pass_rate']:.1f}%, and a platform trust score of "
                f"{semantic_metrics['platform_trust_score']:.1f}. "
                f"{context.operational_context.get('run_history', {}).get('trend_summary', 'Recent trend data is limited.')} "
                f"{self._project_change_highlight(context, fallback='No project-level contributor change is available yet.')} "
                "The current emphasis should remain on turning this controlled foundation into repeatable "
                "stakeholder-facing delivery."
            ),
            fallback_bullets=bullets,
        )

    def executive_summary(self, context: GenAIContext) -> GenAIArtifact:
        focus = (
            f"{len(context.projects)} portfolio assets, {len(context.repository_registry)} registered repositories, "
            f"and a governed analytics surface backed by contracts, quality checks, and delivery endpoints."
        )
        bullets = [
            "Business value comes from making analytics assets more decision-ready and easier to consume.",
            "The operating model combines semantic metrics, governed quality, and reusable delivery surfaces.",
            self._project_change_highlight(
                context,
                fallback=context.operational_context.get("run_history", {}).get(
                    "trend_summary",
                    "Primary modernization lever: expand real integrations and downstream adoption signals.",
                ),
            ),
        ]
        return self._generate_artifact(
            use_case="executive_summary",
            title="Executive Summary",
            prompt_name="executive_summary.md",
            focus=focus,
            context=context,
            parameters={},
            fallback_narrative=(
                "This portfolio operates as an analytics product platform rather than a collection of notebooks. "
                "It combines contracts, metrics, observability, service interfaces, and governed artifacts into "
                "a reusable foundation that supports executive reporting and technical review. "
                f"{context.operational_context.get('snapshot_history', {}).get('comparison_summary', '')} "
                f"{self._project_change_highlight(context, fallback='')}".strip()
            ),
            fallback_bullets=bullets,
        )

    def anomaly_explanation_draft(self, context: GenAIContext) -> GenAIArtifact:
        pass_rate = float(context.quality_report.get("pass_rate", 0.0))
        freshness_issues = self._stale_assets(context)
        if pass_rate < 100:
            concern = "quality variance"
        elif freshness_issues:
            concern = "stale analytical artifact"
        else:
            concern = "governance drift"
        focus = f"Primary anomaly candidate: {concern}. Current pass rate is {pass_rate:.1f}%."
        bullets = [
            f"Observed anomaly candidate: {concern}.",
            self._anomaly_cause_hint(concern, freshness_issues),
            self._anomaly_action_hint(context, concern),
        ]
        return self._generate_artifact(
            use_case="anomaly_explanation_draft",
            title="Anomaly Explanation Draft",
            prompt_name="anomaly_explanation_draft.md",
            focus=focus,
            context=context,
            parameters={"anomaly_candidate": concern},
            fallback_narrative=(
                f"No severe anomaly is confirmed by the current sample run, but the platform should treat "
                f"{concern} as the first investigation path when pass rate, trust score, or artifact freshness "
                "deteriorates. A disciplined response starts with validating contracts, freshness, and upstream "
                "data assumptions."
            ),
            fallback_bullets=bullets,
        )

    def metric_definition_assistant(self, context: GenAIContext, metric_name: str) -> GenAIArtifact:
        metric_definition = self._lookup_metric_definition(context, metric_name)
        focus = f"Explain metric `{metric_name}` for analysts, BI consumers, and leadership."
        bullets = [
            f"Owner: {metric_definition.get('owner', 'unknown')}.",
            f"Category: {metric_definition.get('category', 'unknown')}.",
            f"Formula: {metric_definition.get('formula', 'not documented')}.",
        ]
        return self._generate_artifact(
            use_case="metric_definition_assistant",
            title="Metric Definition Assistant",
            prompt_name="metric_definition_assistant.md",
            focus=focus,
            context=context,
            parameters={"metric_name": metric_name, "metric_definition": metric_definition},
            fallback_narrative=(
                f"{metric_name} is documented as a governed semantic metric intended to align analytics producers "
                f"and consumers on one business-ready definition. Current owner: {metric_definition.get('owner', 'unknown')}. "
                "Its interpretation should always include owner, formula, and business decision context."
            ),
            fallback_bullets=bullets,
        )

    def business_glossary_explanation(self, context: GenAIContext, term: str) -> GenAIArtifact:
        metric_definition = self._lookup_metric_definition(context, term)
        focus = f"Translate glossary term `{term}` into business language without losing technical precision."
        bullets = [
            "Use this explanation for cross-functional stakeholders, not only data practitioners.",
            "Tie the term to decisions, accountability, and expected operational usage.",
            f"Current mapped owner: {metric_definition.get('owner', 'unknown')}.",
        ]
        return self._generate_artifact(
            use_case="business_glossary_explanation",
            title="Business Glossary Explanation",
            prompt_name="business_glossary_explanation.md",
            focus=focus,
            context=context,
            parameters={"term": term, "definition": metric_definition},
            fallback_narrative=(
                f"In this platform, `{term}` is part of the governed analytics vocabulary used to make delivery "
                "consistent across engineering, BI, and leadership discussions. The goal is not only definition "
                "clarity, but also clearer accountability for how a metric supports decisions."
            ),
            fallback_bullets=bullets,
        )

    def pipeline_dataset_description(self, context: GenAIContext, dataset_name: str) -> GenAIArtifact:
        focus = (
            f"Describe dataset `{dataset_name}` generated by the platform pipeline, including purpose, sources, "
            "and downstream consumption."
        )
        bullets = [
            self._dataset_input_bullet(context, dataset_name),
            self._dataset_output_bullet(context, dataset_name),
            "This description should be suitable for onboarding, operations, and data consumers.",
        ]
        return self._generate_artifact(
            use_case="pipeline_dataset_description",
            title="Pipeline and Dataset Description",
            prompt_name="pipeline_dataset_description.md",
            focus=focus,
            context=context,
            parameters={"dataset_name": dataset_name},
            fallback_narrative=(
                f"{dataset_name} is a governed output produced by the canonical portfolio pipeline. It consolidates "
                "portfolio project signals, quality results, semantic metrics, repository metadata, and AI-assisted "
                "drafts so downstream consumers can query a single decision-ready analytical surface."
            ),
            fallback_bullets=bullets,
        )

    def _generate_artifact(
        self,
        use_case: str,
        title: str,
        prompt_name: str,
        focus: str,
        context: GenAIContext,
        parameters: dict[str, Any],
        fallback_narrative: str,
        fallback_bullets: list[str],
    ) -> GenAIArtifact:
        prompt_reference, prompt_text = self._load_prompt(prompt_name)
        task = GenAITaskRequest(
            use_case=use_case,
            prompt_name=prompt_name,
            title=title,
            focus=focus,
            context=context,
            parameters=parameters,
        )
        fallback = ProviderResult(
            narrative=fallback_narrative,
            bullets=fallback_bullets,
            provider_status="local_template",
            generation_mode="template",
        )
        result = self.provider.generate(task, prompt_text, fallback)
        return GenAIArtifact(
            use_case=use_case,
            title=title,
            narrative=result.narrative,
            bullets=result.bullets,
            provider_status=result.provider_status,
            provider_name=self.provider.provider_name,
            model=self.settings.genai_model,
            prompt_reference=prompt_reference,
            generation_mode=result.generation_mode,
        )

    def _build_provider(self) -> TemplateGenAIProvider | OpenAICompatibleGenAIProvider:
        if self.settings.genai_provider == "openai-compatible":
            return OpenAICompatibleGenAIProvider(
                model=self.settings.genai_model,
                base_url=self.settings.genai_base_url,
                api_key=self.settings.genai_api_key,
                timeout_seconds=self.settings.genai_timeout_seconds,
                max_retries=self.settings.genai_max_retries,
            )
        return TemplateGenAIProvider()

    def _load_prompt(self, prompt_name: str) -> tuple[str, str]:
        path = self.prompt_dir / prompt_name
        lines = path.read_text(encoding="utf-8").splitlines()
        prompt_reference = lines[0].strip("# ").strip() if lines else prompt_name
        return prompt_reference, "\n".join(lines)

    def _select_primary_metric(self, context: GenAIContext) -> str:
        metrics = self._metric_definitions(context)
        if metrics:
            return str(metrics[0].get("name", "decision_readiness_score"))
        return "decision_readiness_score"

    def _lookup_metric_definition(self, context: GenAIContext, metric_name: str) -> dict[str, Any]:
        for metric in self._metric_definitions(context):
            if metric.get("name") == metric_name:
                return metric
        return {
            "name": metric_name,
            "description": "Metric not found in the current catalog.",
            "formula": "unknown",
            "owner": "unknown",
            "category": "unknown",
        }

    def _metric_definitions(self, context: GenAIContext) -> list[dict[str, Any]]:
        definitions = context.metric_catalog.get("definitions")
        if isinstance(definitions, list):
            return definitions
        metrics = context.metric_catalog.get("metrics")
        if isinstance(metrics, list):
            return metrics
        return []

    def _stale_assets(self, context: GenAIContext) -> list[str]:
        stale: list[str] = []
        for asset_name, payload in context.operational_context.get("freshness", {}).get("artifacts", {}).items():
            age = payload.get("age_seconds")
            if isinstance(age, (int, float)) and age > 3600:
                stale.append(str(asset_name))
        return stale

    def _anomaly_cause_hint(self, concern: str, freshness_issues: list[str]) -> str:
        if concern == "stale analytical artifact" and freshness_issues:
            return f"Likely root cause: artifact freshness drift affecting {', '.join(freshness_issues[:2])}."
        if concern == "quality variance":
            return "Likely root causes should be validated against failing checks, contract breaks, or source changes."
        return "Likely root causes should be validated against data freshness, contract breaks, or score volatility."

    def _anomaly_action_hint(self, context: GenAIContext, concern: str) -> str:
        stability = context.operational_context.get("run_history", {}).get("stability", "unknown")
        structural_summary = context.operational_context.get("snapshot_history", {}).get("comparison_summary", "")
        if concern == "stale analytical artifact":
            return "Recommended action: refresh the stale artifact path, rerun the pipeline, and compare the next snapshot delta."
        if stability == "volatile":
            return (
                "Recommended action: compare the latest two runs, inspect upstream changes, and validate metric deltas "
                f"before escalation. {self._project_change_highlight(context, fallback='')}".strip()
            )
        if structural_summary and "stable" not in structural_summary.lower():
            return f"Recommended action: review structural differences across snapshots. {structural_summary}"
        return "Recommended action: review latest run artifacts and validate upstream assumptions before escalation."

    def _dataset_input_bullet(self, context: GenAIContext, dataset_name: str) -> str:
        lineage = context.operational_context.get("lineage", {}).get(dataset_name, [])
        if lineage:
            return f"Primary inputs for `{dataset_name}`: {', '.join(str(item) for item in lineage)}."
        return "Primary inputs come from portfolio registry, quality rules, semantic metrics, and repository metadata."

    def _dataset_output_bullet(self, context: GenAIContext, dataset_name: str) -> str:
        freshness = context.operational_context.get("freshness", {}).get("artifacts", {}).get(dataset_name, {})
        updated_at = freshness.get("updated_at_utc")
        if updated_at:
            return f"Latest known artifact update for `{dataset_name}`: {updated_at}."
        return "Generated artifacts support API, Streamlit, warehouse, and contract validation surfaces."

    def _project_change_highlight(self, context: GenAIContext, fallback: str) -> str:
        changes = (
            context.operational_context.get("snapshot_history", {})
            .get("project_change_summary", {})
            .get("changes", [])
        )
        if not changes:
            return fallback

        changed = [item for item in changes if item.get("change_type") == "changed"]
        added = [item for item in changes if item.get("change_type") == "added"]
        removed = [item for item in changes if item.get("change_type") == "removed"]

        if changed:
            item = changed[0]
            return f"Primary project-level movement: {item.get('project_name')} changed ({item.get('detail')})."
        if added:
            item = added[0]
            return f"Primary project-level movement: {item.get('project_name')} was added to the latest snapshot."
        if removed:
            item = removed[0]
            return f"Primary project-level movement: {item.get('project_name')} was removed from the latest snapshot."
        return fallback


def build_genai_suite(
    settings: Settings,
    *,
    projects: list[dict[str, Any]],
    quality_report: dict[str, Any],
    semantic_metrics: dict[str, float],
    metric_catalog: dict[str, Any],
    repository_registry: list[dict[str, Any]],
    operational_context: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    service = AnalyticsGenAIService(settings)
    context = GenAIContext(
        projects=projects,
        quality_report=quality_report,
        semantic_metrics=semantic_metrics,
        metric_catalog=metric_catalog,
        repository_registry=repository_registry,
        operational_context=operational_context,
    )
    return service.build_suite(context)
