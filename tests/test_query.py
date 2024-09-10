import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.parameters import Query
from aiohttp_extracts.wrappers import with_extraction


async def handle_query(a: Query[int], b: Query[int]) -> web.Response:
    return web.json_response({"result": a + b})


@with_extraction
async def get_query_with_defaults(a: Query[int], b: Query[int] = 10) -> web.Response:
    return await handle_query(a, b)


@with_extraction
async def get_query_no_defaults(a: Query[int], b: Query[int]) -> web.Response:
    return await handle_query(a, b)


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/query-defaults", get_query_with_defaults)
    app.router.add_get("/query-no-defaults", get_query_no_defaults)
    return await aiohttp_client(app)


async def send_request_and_assert(
    client: TestClient,
    endpoint: str,
    params: dict,
    expected_status: int,
    expected_text: str = None,
    expected_result: int = None,
):
    response = await client.get(endpoint, params=params)
    assert response.status == expected_status
    if expected_status == 200:
        json_data = await response.json()
        assert json_data["result"] == expected_result
    elif expected_text:
        assert expected_text in await response.text()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint, params, expected_status, expected_text, expected_result",
    [
        ("/query-defaults", {"a": 5, "b": 10}, 200, None, 15),
        ("/query-defaults", {"a": 5}, 400, "Missing query parameter 'b'", None),
        ("/query-no-defaults", {"a": 5, "b": 5}, 200, None, 10),
        ("/query-no-defaults", {"a": 5}, 400, "Missing query parameter 'b'", None),
        ("/query-no-defaults", {"b": 5}, 400, "Missing query parameter 'a'", None),
        (
            "/query-no-defaults",
            {"a": "invalid", "b": 5},
            400,
            "Invalid type for query parameter 'a'. Expected int.",
            None,
        ),
        (
            "/query-no-defaults",
            {"a": 5, "b": "invalid"},
            400,
            "Invalid type for query parameter 'b'. Expected int.",
            None,
        ),
    ],
)
async def test_query_parameters(
    client: TestClient,
    endpoint,
    params,
    expected_status,
    expected_text,
    expected_result,
):
    await send_request_and_assert(
        client, endpoint, params, expected_status, expected_text, expected_result
    )


@pytest.mark.asyncio
async def test_get_query_no_params(client: TestClient):
    await send_request_and_assert(
        client, "/query-no-defaults", {}, 400, "Missing query parameter 'a'"
    )
