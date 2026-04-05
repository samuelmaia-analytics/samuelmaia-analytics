from __future__ import annotations

from config.settings import Settings


def build_runtime_config_summary(settings: Settings) -> dict[str, object]:
    auth_mode = "jwt" if settings.jwt_enabled else "api_key"
    return {
        "environment": settings.env,
        "log_level": settings.log_level,
        "auth": {
            "mode": auth_mode,
            "jwt_enabled": settings.jwt_enabled,
            "jwt_issuer": settings.jwt_issuer,
            "jwt_audience": settings.jwt_audience,
            "api_key_count": len(settings.service_api_keys),
            "rate_limit_per_minute": settings.service_rate_limit,
        },
        "genai": {
            "provider": settings.genai_provider,
            "model": settings.genai_model,
            "base_url_configured": bool(settings.genai_base_url),
            "api_key_configured": bool(settings.genai_api_key),
            "timeout_seconds": settings.genai_timeout_seconds,
            "max_retries": settings.genai_max_retries,
        },
        "change_driver_thresholds": {
            "watch": settings.change_watch_threshold,
            "material": settings.change_material_threshold,
            "critical": settings.change_critical_threshold,
        },
        "paths": {
            "data_dir": str(settings.data_dir),
            "artifacts_dir": str(settings.artifacts_dir),
            "observability_dir": str(settings.observability_dir),
            "warehouse_path": str(settings.warehouse_path),
            "semantic_metrics_path": str(settings.semantic_metrics_path),
            "quality_rules_path": str(settings.quality_rules_path),
            "project_registry_path": str(settings.project_registry_path),
        },
    }
