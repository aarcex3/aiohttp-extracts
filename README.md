# Aiohttp Extracts

This is a forked of the orinial project at [aiohttp-extracts](https://github.com/jorektheglitch/aiohttp-extracts).
Refactored, tested and with new features.

## Header

```python
from aiohttp import web

from aiohttp_extracts import Header, with_extraction


# with extraction
@with_extraction
async def get_header(x_custom: Header) -> web.Response:
    return web.json_response({"x_custom": x_custom})


# without extraction
async def get_header_normal(request: web.Request) -> web.Response:
    x_custom: str = request.headers.get("X-Custom")
    return web.json_response({"x_custom": x_custom})


app = web.Application()
app.add_routes([web.get("/header", get_header)])

if __name__ == "__main__":
    web.run_app(app)

```

## Cookie

```python
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

```

## File

```python
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

```

## Path

```python
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

```

## ReqBody

```python
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

```

## RequestAttr

```python
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
```

You can either user the variable as a name or provide your own, or even specify a type, like:

```python
from aiohttp import web

from aiohttp_extracts import Header, Query, with_extraction


@with_extraction    
async def get_header(user_agent: Header, x_custom: Header["X-Custom"]) -> web.Response:
    return web.json_response({"user-agent": user_agent, "x_custom": x_custom})

@with_extraction
async def get_query_param(page: Query[int]) -> web.Response:  #The query must be an int 
    return web.json_response({"page": page})

```
