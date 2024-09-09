from aiohttp import web

from aiohttp_extracts import ReqBody, with_extraction


# with extraction
@with_extraction
async def get_body(body: ReqBody) -> web.Response:
    return web.json_response(body)


# without extraction
async def get_body_normal(request: web.Request) -> web.Response:
    body = await request.json()
    return web.json_response(body)


app = web.Application()
app.add_routes([web.post("/body", get_body)])

if __name__ == "__main__":
    web.run_app(app)
