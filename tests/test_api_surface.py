from __future__ import annotations

import jwt
from fastapi.testclient import TestClient

from config.settings import get_settings
from services.api.main import app
from services.api.security import reset_rate_limiter


def test_api_metrics_and_repositories_surfaces() -> None:
    reset_rate_limiter(limit=30)
    client = TestClient(app)
    headers = {"X-API-Key": "portfolio-demo-key"}
    metrics_response = client.get("/metrics", headers=headers)
    runtime_config_response = client.get("/governance/runtime-config", headers=headers)
    policy_checks_response = client.get("/governance/policy-checks", headers=headers)
    analytics_checks_response = client.get("/governance/analytics-engineering", headers=headers)
    history_response = client.get("/metrics/history", headers=headers)
    domain_history_response = client.get("/metrics/domain-history", headers=headers)
    project_history_response = client.get("/metrics/project-history", headers=headers)
    repositories_response = client.get("/repositories", headers=headers)
    genai_response = client.get("/genai", headers=headers)
    change_drivers_response = client.get("/change-drivers", headers=headers)

    assert metrics_response.status_code == 200
    assert runtime_config_response.status_code == 200
    assert policy_checks_response.status_code == 200
    assert analytics_checks_response.status_code == 200
    assert history_response.status_code == 200
    assert domain_history_response.status_code == 200
    assert project_history_response.status_code == 200
    assert repositories_response.status_code == 200
    assert genai_response.status_code == 200
    assert change_drivers_response.status_code == 200
    assert "headline" in metrics_response.json()
    assert "change_driver_thresholds" in runtime_config_response.json()
    assert "checks" in policy_checks_response.json()
    assert "models_built" in analytics_checks_response.json()
    assert "series" in history_response.json()
    assert "series" in domain_history_response.json()
    assert "changes" in project_history_response.json()
    assert len(repositories_response.json()["projects"]) >= 1
    assert "changes" in repositories_response.json()
    assert "executive_summary" in genai_response.json()["artifacts"]
    assert "drivers" in change_drivers_response.json()


def test_api_requires_key_for_protected_endpoints() -> None:
    reset_rate_limiter(limit=30)
    client = TestClient(app)
    response = client.get("/metrics")
    assert response.status_code == 401


def test_api_rate_limit_is_enforced() -> None:
    reset_rate_limiter(limit=1)
    client = TestClient(app)
    headers = {"X-API-Key": "portfolio-demo-key"}
    first = client.get("/metrics", headers=headers)
    second = client.get("/metrics", headers=headers)
    assert first.status_code == 200
    assert second.status_code == 429


def test_api_scope_is_enforced(monkeypatch) -> None:
    monkeypatch.setenv("PORTFOLIO_SERVICE_API_KEYS", "portfolio-demo-key,restricted-key")
    monkeypatch.setenv(
        "PORTFOLIO_SERVICE_API_KEY_SCOPES",
        "portfolio-demo-key:snapshot,metrics,insights,repositories,admin;restricted-key:metrics",
    )
    get_settings.cache_clear()
    reset_rate_limiter(limit=30)
    client = TestClient(app)
    response = client.get("/repositories", headers={"X-API-Key": "restricted-key"})
    assert response.status_code == 403
    get_settings.cache_clear()


def test_api_accepts_jwt_when_enabled(monkeypatch) -> None:
    secret = "test-secret-portfolio-jwt-00000001"
    monkeypatch.setenv("PORTFOLIO_JWT_ENABLED", "true")
    monkeypatch.setenv("PORTFOLIO_JWT_SECRET", secret)
    monkeypatch.setenv("PORTFOLIO_JWT_ISSUER", "samuelmaia-analytics")
    monkeypatch.setenv("PORTFOLIO_JWT_AUDIENCE", "portfolio-platform")
    get_settings.cache_clear()
    reset_rate_limiter(limit=30)

    token = jwt.encode(
        {
            "sub": "jwt-user",
            "iss": "samuelmaia-analytics",
            "aud": "portfolio-platform",
            "scopes": ["metrics"],
        },
        secret,
        algorithm="HS256",
    )
    client = TestClient(app)
    response = client.get("/metrics", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    get_settings.cache_clear()


def test_jwt_secret_must_meet_minimum_length(monkeypatch) -> None:
    monkeypatch.setenv("PORTFOLIO_JWT_ENABLED", "true")
    monkeypatch.setenv("PORTFOLIO_JWT_SECRET", "short-secret")
    get_settings.cache_clear()

    try:
        try:
            get_settings()
        except ValueError as exc:
            assert "at least 32 characters" in str(exc)
        else:
            raise AssertionError("Expected JWT secret validation to fail.")
    finally:
        get_settings.cache_clear()
