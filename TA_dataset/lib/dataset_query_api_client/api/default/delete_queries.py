# -*- coding: utf-8 -*-
from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    forward_tag: str,
) -> Dict[str, Any]:
    url = "{}/v2/api/queries/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()
    proxies: Dict[str, str] = client.get_proxy()

    headers["x-dataset-query-forward-tag"] = forward_tag

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "proxies": proxies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.NO_CONTENT:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    forward_tag: str,
) -> Response[Any]:
    """Delete query

     Remove query from the list of launched queries, subsequent pings with token to that query should
    return not found response

    Args:
        id (str):  Example: eyJ0eXBlIjoiTE9HIiwidG9rZW4iOiJxYXRlc3RpbmctbG9nLTF6XzE3OjM5OjMxLjIyMV
            8yMzgzY19mZjAzMjEwYyJ9.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        forward_tag=forward_tag,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
) -> Response[Any]:
    """Delete query

     Remove query from the list of launched queries, subsequent pings with token to that query should
    return not found response

    Args:
        id (str):  Example: eyJ0eXBlIjoiTE9HIiwidG9rZW4iOiJxYXRlc3RpbmctbG9nLTF6XzE3OjM5OjMxLjIyMV
            8yMzgzY19mZjAzMjEwYyJ9.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
