import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.parameters import Cookie
from aiohttp_extracts.wrappers import with_extraction


@with_extraction
async def get_cookie(my_cookie: Cookie) -> web.Response:
    return web.json_response({"cookie": my_cookie})


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/cookie", get_cookie)

    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_get_cookie(client: TestClient):
    response = await client.get("/cookie", cookies={"my_cookie": "test-value"})
    assert response.status == 200

    json_data = await response.json()
    assert json_data["cookie"] == "test-value"
