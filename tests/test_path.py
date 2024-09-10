import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.parameters import Path
from aiohttp_extracts.wrappers import with_extraction


@with_extraction
async def get_path(a: Path[int], b: Path[int]) -> web.Response:
    return web.json_response({"result": a + b})


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/path/{a}/{b}", get_path)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_path(client: TestClient):
    response = await client.get(f"/path/{4}/{10}")
    assert response.status == 200

    json_data = await response.json()
    assert json_data["result"] == 14


@pytest.mark.asyncio
async def test_path_invalid_type(client: TestClient):
    response = await client.get(f"/path/{4}/g")
    assert response.status == 400
    assert "Invalid type for path parameter 'b'. Expected int." in await response.text()


@pytest.mark.asyncio
async def test_path_missing_param(client: TestClient):
    response = await client.get(f"/path/{4}")
    assert response.status == 404
