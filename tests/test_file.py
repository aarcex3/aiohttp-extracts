import io

import pytest
from aiohttp import web
from pytest_aiohttp.plugin import TestClient

from aiohttp_extracts.parameters import File
from aiohttp_extracts.wrappers import with_extraction


@with_extraction
async def get_file(file: File) -> web.Response:
    return web.json_response(
        {"filename": file.filename, "content": file.content.decode()}
    )


@pytest.fixture
async def client(aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_post("/file", get_file)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_file(client: TestClient):

    fake_file = io.BytesIO(b"This is a test file.")
    fake_file.name = "test.txt"

    data = {"file": fake_file}
    response = await client.post("/file", data=data)
    assert response.status == 200

    json_data = await response.json()
    assert json_data["filename"] == "test.txt"
    assert json_data["content"] == "This is a test file."
