from aiohttp import web

from aiohttp_extracts import RequestAttr, with_extraction


# with extraction
@with_extraction
async def get_request_attr(user: RequestAttr) -> web.Response:
    return web.json_response({"user": user})


# without extraction
async def get_request_attr_normal(request: web.Request) -> web.Response:
    user = request.get("user")
    return web.json_response({"user": user})


app = web.Application()
app.add_routes([web.get("/user", get_request_attr)])

if __name__ == "__main__":
    web.run_app(app)
