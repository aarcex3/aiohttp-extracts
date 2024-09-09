from aiohttp import web

from aiohttp_extracts import Query, with_extraction


# with extraction
@with_extraction
async def get_query_param(page: Query[int]) -> web.Response:  # You can specify a type
    return web.json_response({"page": page})


# without extraction
async def get_query_param_normal(request: web.Request) -> web.Response:
    page: str = request.query.get("page")
    return web.json_response({"page": page})


app = web.Application()
app.add_routes([web.get("/query", get_query_param)])

if __name__ == "__main__":
    web.run_app(app)
