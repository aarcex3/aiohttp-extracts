from aiohttp import web

from aiohttp_extracts import File, with_extraction


# with extraction
@with_extraction
async def get_file(upload: File) -> web.Response:
    if upload:
        return web.json_response({"filename": upload.filename})
    return web.json_response({"error": "No file uploaded"})


# without extraction
async def get_file_normal(request: web.Request) -> web.Response:
    reader = await request.multipart()
    filename = None

    async for part in reader:
        if part.name == "upload":
            filename = part.filename
            break

    if filename:
        return web.json_response({"filename": filename})
    return web.json_response({"error": "No file uploaded"})


app = web.Application()
app.add_routes([web.post("/upload", get_file)])

if __name__ == "__main__":
    web.run_app(app)
