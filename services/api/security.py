from __future__ import annotations

import time
from collections import defaultdict, deque
from collections.abc import Iterable
from dataclasses import dataclass

import jwt
from fastapi import Header, HTTPException, Request, status

from config.settings import get_settings


@dataclass
class RateLimiter:
    limit: int
    window_seconds: int = 60

    def __post_init__(self) -> None:
        self._buckets: dict[str, deque[float]] = defaultdict(deque)

    def check(self, client_id: str) -> None:
        now = time.time()
        bucket = self._buckets[client_id]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()
        if len(bucket) >= self.limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded for this API key or client.",
            )
        bucket.append(now)


_rate_limiter = RateLimiter(limit=get_settings().service_rate_limit)


def reset_rate_limiter(limit: int | None = None) -> None:
    global _rate_limiter
    _rate_limiter = RateLimiter(limit=limit or get_settings().service_rate_limit)


def require_api_key(
    request: Request,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> str:
    settings = get_settings()
    valid_keys: Iterable[str] = settings.service_api_keys
    if x_api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid API key.",
        )
    client_id = x_api_key or request.client.host if request.client else "unknown"
    _rate_limiter.check(client_id)
    return x_api_key


def require_scope(required_scope: str):
    def dependency(
        request: Request,
        api_key: str = Header(default="", alias="X-API-Key"),
        authorization: str | None = Header(default=None, alias="Authorization"),
    ) -> str:
        validated_key, allowed_scopes = _authenticate_request(request, api_key, authorization)
        if required_scope not in allowed_scopes and "admin" not in allowed_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required scope: {required_scope}",
            )
        return validated_key

    return dependency


def _authenticate_request(
    request: Request,
    api_key: str | None,
    authorization: str | None,
) -> tuple[str, tuple[str, ...]]:
    settings = get_settings()
    if settings.jwt_enabled and authorization:
        token = _extract_bearer_token(authorization)
        claims = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=["HS256"],
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
        )
        client_id = claims.get("sub", "jwt-client")
        _rate_limiter.check(client_id)
        scopes = tuple(claims.get("scopes", []))
        return client_id, scopes

    validated_key = require_api_key(request, api_key)
    scopes = settings.service_api_key_scopes.get(validated_key, ())
    return validated_key, scopes


def _extract_bearer_token(authorization: str) -> str:
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must use Bearer token format.",
        )
    return authorization[len(prefix):].strip()
