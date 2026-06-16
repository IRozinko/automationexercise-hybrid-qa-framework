from __future__ import annotations

import json

import requests

from src.models.user import User

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


class AccountClient:
    """Thin client for Automation Exercise account endpoints."""

    def __init__(self, base_url: str, timeout: float = 15.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(_DEFAULT_HEADERS)

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
        url = f"{self.base_url}{path}"
        try:
            response = self._session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                allow_redirects=False,
                **kwargs,
            )
        except requests.TooManyRedirects as exc:
            raise AssertionError(
                f"Too many redirects calling {url} — the site may be blocking "
                "automated requests or is temporarily unavailable."
            ) from exc
        if response.is_redirect:
            raise AssertionError(
                f"Unexpected redirect ({response.status_code}) from {url} to "
                f"{response.headers.get('location')} — the site may be blocking "
                "automated requests or is temporarily unavailable."
            )
        response.raise_for_status()
        return response

    @staticmethod
    def _payload(response: requests.Response) -> dict:
        try:
            return response.json()
        except json.JSONDecodeError as exc:
            raise AssertionError(f"Unexpected API response: {response.text}") from exc
