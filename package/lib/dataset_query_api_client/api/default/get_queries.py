from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.query_result import QueryResult
from ...types import UNSET, Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    last_step_seen: int,
) -> Dict[str, Any]:
    url = "{}/v2/api/queries/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["lastStepSeen"] = last_step_seen

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, QueryResult]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = QueryResult.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, QueryResult]]:
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
    last_step_seen: int,
) -> Response[Union[Any, QueryResult]]:
    """Ping query

     Retrieve further information from a previously launched query against data stored in one or more
    Dataset accounts.

    Args:
        id (str):  Example: eyJ0eXBlIjoiTE9HIiwidG9rZW4iOiJxYXRlc3RpbmctbG9nLTF6XzE3OjM5OjMxLjIyMV
            8yMzgzY19mZjAzMjEwYyJ9.
        last_step_seen (int):  Example: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResult]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        last_step_seen=last_step_seen,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: str,
    *,
    client: Client,
    last_step_seen: int,
) -> Optional[Union[Any, QueryResult]]:
    """Ping query

     Retrieve further information from a previously launched query against data stored in one or more
    Dataset accounts.

    Args:
        id (str):  Example: eyJ0eXBlIjoiTE9HIiwidG9rZW4iOiJxYXRlc3RpbmctbG9nLTF6XzE3OjM5OjMxLjIyMV
            8yMzgzY19mZjAzMjEwYyJ9.
        last_step_seen (int):  Example: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResult]
    """

    return sync_detailed(
        id=id,
        client=client,
        last_step_seen=last_step_seen,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    last_step_seen: int,
) -> Response[Union[Any, QueryResult]]:
    """Ping query

     Retrieve further information from a previously launched query against data stored in one or more
    Dataset accounts.

    Args:
        id (str):  Example: eyJ0eXBlIjoiTE9HIiwidG9rZW4iOiJxYXRlc3RpbmctbG9nLTF6XzE3OjM5OjMxLjIyMV
            8yMzgzY19mZjAzMjEwYyJ9.
        last_step_seen (int):  Example: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, QueryResult]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        last_step_seen=last_step_seen,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    last_step_seen: int,
) -> Optional[Union[Any, QueryResult]]:
    """Ping query

     Retrieve further information from a previously launched query against data stored in one or more
    Dataset accounts.

    Args:
        id (str):  Example: eyJ0eXBlIjoiTE9HIiwidG9rZW4iOiJxYXRlc3RpbmctbG9nLTF6XzE3OjM5OjMxLjIyMV
            8yMzgzY19mZjAzMjEwYyJ9.
        last_step_seen (int):  Example: 50.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, QueryResult]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            last_step_seen=last_step_seen,
        )
    ).parsed
