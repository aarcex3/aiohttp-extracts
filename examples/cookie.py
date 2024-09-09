from aiohttp import web

from aiohttp_extracts import Cookie, with_extraction


# with extraction
@with_extraction
async def get_cookie(session_id: Cookie) -> web.Response:
    return web.json_response({"session_id": session_id})


# without extraction
async def get_cookie_normal(request: web.Request) -> web.Response:
    session_id: str = request.cookies.get("session_id")
    return web.json_response({"session_id": session_id})


app = web.Application()
app.add_routes([web.get("/cookie", get_cookie)])

if __name__ == "__main__":
    web.run_app(app)
