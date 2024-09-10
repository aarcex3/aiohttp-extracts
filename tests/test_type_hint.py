import pytest
from aiohttp import ClientResponseError, web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts import with_extraction
from aiohttp_extracts.wrappers import fetch_fn_params


@with_extraction
async def get_no_type(a) -> web.Response:
    return web.json_response(a)


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/no-type", get_no_type)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_no_type(client: TestClient):
    with pytest.raises(
        ValueError,
    ):
        fetch_fn_params(get_no_type)
        await client.get("/no-type")
