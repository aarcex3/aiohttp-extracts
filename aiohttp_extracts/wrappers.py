import inspect
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, Union

from aiohttp import web
from aiohttp.web_urldispatcher import UrlMappingMatchInfo

from .parameters import Parameter

AsyncFunc = Callable[..., Awaitable[web.Response]]
FunctionParams = Dict[
    str, Tuple[Union[Type[web.Request], Type[Parameter], Type[type]], Optional[Any]]
]


def fetch_fn_params(fn: Callable) -> FunctionParams:
    fn_params = {}
    params = inspect.signature(fn).parameters
    for param_name, param in params.items():
        # if param_name == "self":
        #     continue
        annotation = param.annotation
        default = param.default
        if default is param.empty:
            default = None
        if annotation is param.empty:
            raise ValueError(
                f"Parameter '{param_name}' of function '{fn.__name__}' has no type hint"
            )
        fn_params[param_name] = (annotation, default)

    return fn_params


async def handle_request(
    func: Callable, request: web.Request, kwargs: Dict[str, Any]
) -> Callable:
    async def wrapper(*args, **kwargs):
        func_params: FunctionParams = fetch_fn_params(func)
        path_params: UrlMappingMatchInfo = request.match_info
        kwargs.update(path_params)
        for name, (param_type, default) in func_params.items():
            if param_type is web.Request:
                kwargs[name] = request
            elif issubclass(param_type, Parameter) and isinstance(param_type, Type):
                kwargs[name] = (
                    await param_type.extract(name=name, request=request) or default
                )

            else:
                kwargs[name] = kwargs.get(name, default)

        return await func(*args, **kwargs)

    return wrapper


def extraction_wrapper(fn: AsyncFunc) -> AsyncFunc:
    @wraps(fn)
    async def wrapped(request: web.Request, *args, **kwargs) -> web.Response:
        func_with_params = await handle_request(fn, request, kwargs)
        return await func_with_params(*args, **kwargs)

    return wrapped


def with_extraction(handler: AsyncFunc) -> AsyncFunc:
    return extraction_wrapper(handler)
