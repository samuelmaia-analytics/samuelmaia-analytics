from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    env: str
    log_level: str
    data_dir: Path
    artifacts_dir: Path
    observability_dir: Path
    warehouse_path: Path
    genai_prompt_dir: Path
    semantic_metrics_path: Path
    quality_rules_path: Path
    genai_prompt_path: Path
    raw_portfolio_path: Path
    project_registry_path: Path
    genai_provider: str
    genai_model: str
    genai_base_url: str
    genai_api_key: str
    genai_timeout_seconds: int
    genai_max_retries: int
    service_api_keys: tuple[str, ...]
    service_api_key_scopes: dict[str, tuple[str, ...]]
    service_rate_limit: int
    jwt_enabled: bool
    jwt_secret: str
    jwt_issuer: str
    jwt_audience: str
    change_watch_threshold: float
    change_material_threshold: float
    change_critical_threshold: float


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    root = Path(__file__).resolve().parents[1]
    data_dir = root / os.getenv("PORTFOLIO_DATA_DIR", "data")
    artifacts_dir = root / os.getenv("PORTFOLIO_ARTIFACTS_DIR", "data/processed")
    observability_dir = root / os.getenv("PORTFOLIO_OBSERVABILITY_DIR", "data/observability")
    api_keys = tuple(
        key.strip()
        for key in os.getenv("PORTFOLIO_SERVICE_API_KEYS", "portfolio-demo-key").split(",")
        if key.strip()
    )
    api_key_scopes: dict[str, tuple[str, ...]] = {}
    raw_scope_map = os.getenv(
        "PORTFOLIO_SERVICE_API_KEY_SCOPES",
        "portfolio-demo-key:snapshot,metrics,insights,repositories,admin",
    )
    for item in raw_scope_map.split(";"):
        item = item.strip()
        if not item or ":" not in item:
            continue
        key, scopes = item.split(":", 1)
        api_key_scopes[key.strip()] = tuple(scope.strip() for scope in scopes.split(",") if scope.strip())
    jwt_enabled = os.getenv("PORTFOLIO_JWT_ENABLED", "false").strip().lower() == "true"
    jwt_secret = os.getenv("PORTFOLIO_JWT_SECRET", "change-me")
    if jwt_enabled and len(jwt_secret) < 32:
        raise ValueError("PORTFOLIO_JWT_SECRET must be at least 32 characters when JWT auth is enabled.")

    return Settings(
        env=os.getenv("PORTFOLIO_ENV", "dev"),
        log_level=os.getenv("PORTFOLIO_LOG_LEVEL", "INFO"),
        data_dir=data_dir,
        artifacts_dir=artifacts_dir,
        observability_dir=observability_dir,
        warehouse_path=root / os.getenv("PORTFOLIO_WAREHOUSE_PATH", "data/warehouse/portfolio_platform.db"),
        genai_prompt_dir=root / "config" / "prompts" / "genai",
        semantic_metrics_path=root / "config" / "semantic_metrics.json",
        quality_rules_path=root / "config" / "quality_rules.json",
        genai_prompt_path=root / "config" / "prompts" / "genai" / "narrative_kpi_insights.md",
        raw_portfolio_path=data_dir / "raw" / "portfolio_projects.csv",
        project_registry_path=root / "config" / "project_registry.json",
        genai_provider=os.getenv("PORTFOLIO_GENAI_PROVIDER", "local-template"),
        genai_model=os.getenv("PORTFOLIO_GENAI_MODEL", "gpt-portfolio-analyst"),
        genai_base_url=os.getenv("PORTFOLIO_GENAI_BASE_URL", "").strip(),
        genai_api_key=os.getenv("PORTFOLIO_GENAI_API_KEY", "").strip(),
        genai_timeout_seconds=int(os.getenv("PORTFOLIO_GENAI_TIMEOUT_SECONDS", "10")),
        genai_max_retries=int(os.getenv("PORTFOLIO_GENAI_MAX_RETRIES", "2")),
        service_api_keys=api_keys,
        service_api_key_scopes=api_key_scopes,
        service_rate_limit=int(os.getenv("PORTFOLIO_SERVICE_RATE_LIMIT", "30")),
        jwt_enabled=jwt_enabled,
        jwt_secret=jwt_secret,
        jwt_issuer=os.getenv("PORTFOLIO_JWT_ISSUER", "samuelmaia-analytics"),
        jwt_audience=os.getenv("PORTFOLIO_JWT_AUDIENCE", "portfolio-platform"),
        change_watch_threshold=float(os.getenv("PORTFOLIO_CHANGE_WATCH_THRESHOLD", "1.0")),
        change_material_threshold=float(os.getenv("PORTFOLIO_CHANGE_MATERIAL_THRESHOLD", "3.0")),
        change_critical_threshold=float(os.getenv("PORTFOLIO_CHANGE_CRITICAL_THRESHOLD", "5.0")),
    )
