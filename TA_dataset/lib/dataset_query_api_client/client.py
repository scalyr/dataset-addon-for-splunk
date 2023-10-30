# -*- coding: utf-8 -*-
import platform
import ssl
from pathlib import Path
from typing import Dict, Union

import attr
import httpx
import requests


@attr.s(auto_attribs=True)
class Client:
    """A class for keeping track of data related to the API

    Attributes:
        base_url: The base URL for the API, all requests are made to a relative path to this URL
        cookies: A dictionary of cookies to be sent with every request
        headers: A dictionary of headers settings to be used for every request
        proxy: A dictionary of proxy to be sent with every request
        timeout: The maximum amount of a time in seconds a request can take. API functions will raise
            httpx.TimeoutException if this is exceeded.
        verify_ssl: Whether to verify the SSL certificate of the API server. This should be True in production,
            but can be set to False for testing purposes.
        raise_on_unexpected_status: Whether to raise an errors.UnexpectedStatus if the API returns a
            status code that was not documented in the source OpenAPI document.
        follow_redirects: Whether to follow redirects. Default value is False.
    """

    base_url: str
    cookies: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    headers: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    proxy: Dict[str, str] = attr.ib(factory=dict, kw_only=True)
    timeout: float = attr.ib(5.0, kw_only=True)
    verify_ssl: Union[str, bool, ssl.SSLContext] = attr.ib(True, kw_only=True)
    raise_on_unexpected_status: bool = attr.ib(False, kw_only=True)
    follow_redirects: bool = attr.ib(False, kw_only=True)

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in all endpoints"""
        return {**self.headers}

    def with_headers(self, headers: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional headers"""
        return attr.evolve(self, headers={**self.headers, **headers})

    def get_cookies(self) -> Dict[str, str]:
        return {**self.cookies}

    def with_cookies(self, cookies: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        return attr.evolve(self, cookies={**self.cookies, **cookies})

    def get_timeout(self) -> float:
        return self.timeout

    def with_timeout(self, timeout: float) -> "Client":
        """Get a new client matching this one with a new timeout (in seconds)"""
        return attr.evolve(self, timeout=timeout)

    def get_proxy(self) -> Dict[str, str]:
        return {**self.proxy}

    def with_proxy(self, proxy: Dict[str, str]) -> "Client":
        """Get a new client matching this one with additional cookies"""
        return attr.evolve(self, proxy={**self.proxy, **proxy})


def get_user_agent():
    """Get user agent"""

    def extract(f: Path) -> str:
        if not f.exists:
            return str(f.resolve())
        with f.open() as fh:
            return fh.readline().replace("\n", "").replace("\r", "")

    current_file = Path(__file__)
    version_file = current_file.parent.parent.parent / "VERSION"
    version = extract(version_file)

    splunk_version_file = (
        current_file.parent.parent.parent.parent.parent / "splunk.version"
    )
    splunk_version = extract(splunk_version_file)

    return "dataset-splunk-addon;{};{};python-{};splunk-{};requests-{},httpx-{}".format(
        version,
        platform.platform(),
        platform.python_version(),
        splunk_version,
        requests.__version__,
        httpx.__version__,
    )


@attr.s(auto_attribs=True)
class AuthenticatedClient(Client):
    """A Client which has been authenticated for use on secured endpoints"""

    token: str
    prefix: str = "Bearer"
    auth_header_name: str = "Authorization"

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in authenticated endpoints"""
        auth_header_value = f"{self.prefix} {self.token}" if self.prefix else self.token

        return {
            self.auth_header_name: auth_header_value,
            "User-Agent": get_user_agent(),
            **self.headers,
        }
