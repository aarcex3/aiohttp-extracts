from aiohttp import web

from aiohttp_extracts import Header, with_extraction


# with extraction
@with_extraction
async def get_header(x_custom: Header) -> web.Response:
    return web.json_response({"x_custom": x_custom})


# with out extaction
async def get_header_normal(request: web.Request) -> web.Response:
    x_custom: str = request.headers.get("X-Custom")
    return web.json_response({"x_custom": x_custom})


app = web.Application()
app.add_routes([web.get("/header", get_header)])

if __name__ == "__main__":
    web.run_app(app)
