from typing import Optional

import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.parameters import Header
from aiohttp_extracts.wrappers import with_extraction


@with_extraction
async def get_header(x_custom: Header) -> web.Response:
    return web.json_response({"x_custom": x_custom})


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get("/header", get_header)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_header(client: TestClient):
    response = await client.get("/header", headers={"X-Custom": "test-value"})

    assert response.status == 200

    json_data = await response.json()
    assert json_data["x_custom"] == "test-value"


@pytest.mark.asyncio
async def test_header_missing(client: TestClient):
    response = await client.get("/header")

    assert response.status == 400
    assert "Missing header 'X-Custom'" in await response.text()
