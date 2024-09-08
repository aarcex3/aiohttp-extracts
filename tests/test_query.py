import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.parameters import Query
from aiohttp_extracts.wrappers import with_extraction


@with_extraction
async def get_query_with_defaults(
    a: Query[int] = 5, b: Query[int] = 10
) -> web.Response:
    return web.json_response({"result": a + b})


@with_extraction
async def get_query_no_defaults(a: Query[int], b: Query[int]) -> web.Response:
    return web.json_response({"result": a + b})


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/query-defaults", get_query_with_defaults)
    app.router.add_get("/query-no-defualts", get_query_no_defaults)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_get_query_with_defaults(client: TestClient):

    response = await client.get("/query-defaults", params={"a": 5, "b": 10})
    assert response.status == 200
    json_data = await response.json()
    assert json_data["result"] == 15


@pytest.mark.asyncio
async def test_get_query_no_defaults(client: TestClient):

    response = await client.get("/query-no-defualts", params={"a": 5, "b": 5})
    assert response.status == 200
    json_data = await response.json()
    assert json_data["result"] == 10
