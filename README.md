# aiohttp-extracts

This library allows you to extract variable number of request parameters to a handler's arguments.
It uses type hints to determine where each value must be extracted from.

## For example

With aiohttp-extracts:
```python3
from aiohttp import web
from aiohttp_extracts import with_extraction
from aiohttp_extracts import RequestAttr, MatchInfo, QueryAttr


routes = web.RouteTableDef()


@routes.get(r'/chats/{chat_id:(\d+)}/')
@with_extraction
async def handler(
    user: RequestAttr[int],           # by default it uses argument name
    chat: MatchInfo['chat_id', int],  # but you can specify name what you want
    offset: QueryAttr[int] = 0,       # and you can simply set a default value
    count: QueryAttr[int] = 100
) -> web.Response:
    ...
```

Without aiohttp-extracts:
```python3
from aiohttp import web
from aiohttp_extracts import with_extraction


routes = web.RouteTableDef()


@routes.get(r'/chats/{chat_id:(\d+)}/')
async def handler(request: web.Request) -> web.Response:
    user = request.get('user')
    chat = request.match_info.get('chat_id')
    offset = request.query.get('offset', 0)
    count = request.query.get('count', 100)
    ...
```

## Installation

Installation process as simple as:

    $ pip install aiohttp-extracts

## Usage

### Usual handler

```python3
from aiohttp import web
from aiohttp_extracts import with_extraction
from aiohttp_extracts import RequestAttr, MatchInfo, QueryAttr


@with_extraction
async def handler(
    user: RequestAttr[int],
    chat: MatchInfo['chat_id', int],
    offset: QueryAttr[int] = 0,
    count: QueryAttr[int] = 100
) -> web.Response:
    ...
```

### Classview

#### With decorator

```python3
from aiohttp import web
from aiohttp_extracts import with_extraction
from aiohttp_extracts import RequestAttr, MatchInfo, QueryAttr


@extract_classview
class ChatView(web.View):

    async def get(
        user: RequestAttr[int],
        chat: MatchInfo['chat_id', int],
        offset: QueryAttr[int] = 0,
        count: QueryAttr[int] = 100
    ) -> web.Response:
        ...
```

#### With metaclass

```python3
from aiohttp import web
from aiohttp_extracts import ExtractionMeta
from aiohttp_extracts import RequestAttr, MatchInfo, QueryAttr


class ChatView(web.View, metaclass=ExtractionMeta):

    async def get(
        user: RequestAttr[int],
        chat: MatchInfo['chat_id', int],
        offset: QueryAttr[int] = 0,
        count: QueryAttr[int] = 100
    ) -> web.Response:
        ...
```

## Types that can be used in handlers args

| Type name | What it replaces | Additional info |
|:----------|:-----------------|:---------------:|
| aiohttp.web.Request | request | Usually request object |
| aiohttp_extracts.RequestAttr | request.get(...) | Any request attribute |
| aiohttp_extracts.MatchInfo | request.match_info.get(...) | |
| aiohttp_extracts.QueryAttr | request.query.get(...) | |
| aiohttp_extracts.Header | request.headers.get(...) | |
| aiohttp_extracts.Cookie | request.cookies.get(...) | |
| aiohttp_extracts.JSONBody | await request.json() | |

## Links

This library on [PyPI](https://pypi.org/project/aiohttp_extracts/)
