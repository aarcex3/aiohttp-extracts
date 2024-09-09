from aiohttp import web

from aiohttp_extracts import Path, with_extraction


# with extraction
@with_extraction
async def get_path_param(item_id: Path) -> web.Response:
    return web.json_response({"item_id": item_id})


# without extraction
async def get_path_param_normal(request: web.Request) -> web.Response:
    item_id: str = request.match_info.get("item_id")
    return web.json_response({"item_id": item_id})


app = web.Application()
app.add_routes([web.get("/items/{item_id}", get_path_param)])

if __name__ == "__main__":
    web.run_app(app)
