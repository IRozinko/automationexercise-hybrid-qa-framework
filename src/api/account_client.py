from __future__ import annotations

import json

import requests

from src.models.user import User


class AccountClient:
    """Thin client for Automation Exercise account endpoints."""

    def __init__(self, base_url: str, timeout: float = 15.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def create_account(self, user: User) -> None:
        response = self._request("POST", "/api/createAccount", data=user.as_api_payload())
        payload = self._payload(response)
        if payload.get("responseCode") != 201:
            raise AssertionError(f"Account was not created: {payload}")

    def delete_account(self, email: str, password: str) -> None:
        response = self._request(
            "DELETE",
            "/api/deleteAccount",
            data={"email": email, "password": password},
        )
        payload = self._payload(response)
        if payload.get("responseCode") not in {200, 404}:
            raise AssertionError(f"Account was not deleted: {payload}")

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        response = requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            timeout=self.timeout,
            **kwargs,
        )
        response.raise_for_status()
        return response

    @staticmethod
    def _payload(response: requests.Response) -> dict:
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise AssertionError(f"Unexpected API response: {response.text}") from exc
