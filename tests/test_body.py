import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.parameters import ReqBody
from aiohttp_extracts.wrappers import with_extraction


@with_extraction
async def get_body(body: ReqBody) -> web.Response:
    return web.json_response(body)


@with_extraction
async def get_no_body(body: ReqBody) -> web.Response:
    return web.json_response(body)


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/body", get_body)
    app.router.add_get("/no-body", get_no_body)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_body(client: TestClient):
    response = await client.get("/body", json={"X-Custom": "test-value"})
    assert response.status == 200

    json_data = await response.json()
    assert json_data["X-Custom"] == "test-value"


@pytest.mark.asyncio
async def test_no_body(client: TestClient):
    response = await client.get("/no-body")
    assert response.status == 400

    error_message = await response.text()
    assert "Request body is missing." in error_message
