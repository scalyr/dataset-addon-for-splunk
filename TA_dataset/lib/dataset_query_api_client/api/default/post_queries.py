import logging
from http import HTTPStatus
from typing import Any, Dict, Optional

import httpx

from ... import errors
from ...client import Client
from ...models.post_queries_launch_query_request_body import (
    PostQueriesLaunchQueryRequestBody,
)
from ...models.post_queries_launch_query_request_body_query_type import (
    PostQueriesLaunchQueryRequestBodyQueryType,
)
from ...models.query_result import QueryResult
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: PostQueriesLaunchQueryRequestBody,
) -> Dict[str, Any]:
    url = "{}/v2/api/queries".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
    }


def _parse_response(
    *,
    client: Client,
    response: httpx.Response,
    query_type: PostQueriesLaunchQueryRequestBodyQueryType,
) -> Optional[QueryResult]:
    if response.status_code == HTTPStatus.OK:
        try:
            content = response.json()
            logging.info(
                "PARSING RESPONSE FOR QUERY TYPE: {}, CONTENT: {}".format(
                    query_type, repr(content)
                )
            )
            response_200 = QueryResult.from_dict(content, query_type)

            return response_200
        except Exception as inst:
            logging.exception("PARSING ERROR: {}".format(repr(inst)))
            return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *,
    client: Client,
    response: httpx.Response,
    query_type: PostQueriesLaunchQueryRequestBodyQueryType,
) -> Response[QueryResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        # parsed=None
        parsed=_parse_response(client=client, response=response, query_type=query_type),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: PostQueriesLaunchQueryRequestBody,
) -> Response[QueryResult]:
    """Launch a query

     Launches a new query against data stored in one or more Datasets accounts.

    On success returns (possibly incomplete) query results along with a unique query `token` - id which
    can be used to
    send subsequent Ping requests to fetch additional results until the query is completed.

    Args:
        json_body (PostQueriesLaunchQueryRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QueryResult]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )
    # content = response.json()
    # logging.warning("RESPONSE status={}, content={}".format(response.status_code, content))

    return _build_response(
        client=client, response=response, query_type=json_body.query_type
    )


def sync(
    *,
    client: Client,
    json_body: PostQueriesLaunchQueryRequestBody,
) -> Optional[QueryResult]:
    """Launch a query

     Launches a new query against data stored in one or more Datasets accounts.

    On success returns (possibly incomplete) query results along with a unique query `token` - id which
    can be used to
    send subsequent Ping requests to fetch additional results until the query is completed.

    Args:
        json_body (PostQueriesLaunchQueryRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QueryResult
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: PostQueriesLaunchQueryRequestBody,
) -> Response[QueryResult]:
    """Launch a query

     Launches a new query against data stored in one or more Datasets accounts.

    On success returns (possibly incomplete) query results along with a unique query `token` - id which
    can be used to
    send subsequent Ping requests to fetch additional results until the query is completed.

    Args:
        json_body (PostQueriesLaunchQueryRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[QueryResult]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(
        client=client, response=response, query_type=json_body.query_type
    )


async def asyncio(
    *,
    client: Client,
    json_body: PostQueriesLaunchQueryRequestBody,
) -> Optional[QueryResult]:
    """Launch a query

     Launches a new query against data stored in one or more Datasets accounts.

    On success returns (possibly incomplete) query results along with a unique query `token` - id which
    can be used to
    send subsequent Ping requests to fetch additional results until the query is completed.

    Args:
        json_body (PostQueriesLaunchQueryRequestBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        QueryResult
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
