from __future__ import annotations

import requests

from src.models.user import User


class AccountClient:
    """Thin client for Automation Exercise account endpoints."""

    def __init__(self, base_url: str, timeout: float = 15.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def create_account(self, user: User) -> None:
        raise NotImplementedError

    def delete_account(self, email: str, password: str) -> None:
        raise NotImplementedError

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        return requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )
