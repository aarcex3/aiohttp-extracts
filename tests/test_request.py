import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.wrappers import with_extraction


@with_extraction
async def get_request(request: web.Request) -> web.Response:
    message = await request.json()
    return web.json_response(message)


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/request", get_request)

    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_get_cookie(client: TestClient):
    response = await client.get("/request", json={"test": "test"})
    assert response.status == 200
    data = await response.json()
    assert data["test"] == "test"
