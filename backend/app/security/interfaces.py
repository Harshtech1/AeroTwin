"""Authentication and abuse-prevention ports; no policy is implemented here."""

from __future__ import annotations

from typing import Protocol

from starlette.requests import Request


class Principal(Protocol):
    @property
    def subject(self) -> str: ...


class JWTProvider(Protocol):
    async def decode(self, token: str) -> Principal: ...


class OAuthProvider(Protocol):
    async def exchange_code(self, code: str, redirect_uri: str) -> Principal: ...


class APIKeyProvider(Protocol):
    async def authenticate(self, api_key: str) -> Principal: ...


class RateLimiter(Protocol):
    async def is_allowed(self, key: str) -> bool: ...


class AuthenticationProvider(Protocol):
    async def authenticate(self, request: Request) -> Principal | None: ...
