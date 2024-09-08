import inspect
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, Union

from aiohttp import web

from .parameters import Parameter

AsyncFunc = Callable[..., Awaitable[web.Response]]
FunctionParams = Dict[str, Tuple[Union[web.Request, Parameter, Type], Optional[Any]]]


def fetch_fn_params(fn: Callable) -> FunctionParams:
    fn_params = {}
    params = inspect.signature(fn).parameters
    for param_name, param in params.items():
        if param_name == "self":
            continue
        annotation = param.annotation
        default = param.default
        if default is param.empty:
            default = None
        if annotation is param.empty:
            raise ValueError(
                "Parameter {} of function {} has no type hint".format(param_name, fn)
            )
        fn_params[param.name] = (annotation, default)

    return fn_params


def extraction_wrapper(fn: AsyncFunc, classview: bool = False) -> AsyncFunc:
    fn_params: FunctionParams = fetch_fn_params(fn)

    @wraps(fn)
    async def wrapped(request_or_view: Union[web.Request, web.View]) -> web.Response:
        args = []
        if classview:
            request = request_or_view.request  # type: ignore
            args.append(request_or_view)
        else:
            request = request_or_view

        params = {}
        for name, (param_type, default) in fn_params.items():
            try:
                if isinstance(param_type, Type) and issubclass(param_type, web.Request):
                    params[name] = request
                elif isinstance(param_type, Type) and issubclass(param_type, Parameter):

                    params[name] = (
                        await param_type.extract(name=name, request=request) or default
                    )
                else:
                    path_params = request.match_info
                    params[name] = path_params.get(name, default)
            except Exception as e:
                print(f"Error extracting parameter '{name}': {e}")
                params[name] = default
            print(params)
        return await fn(*args, **params)

    return wrapped


def with_extraction(handler: Optional[AsyncFunc] = None, classview: bool = False):
    if handler:
        return extraction_wrapper(handler, classview=classview)
    return extraction_wrapper


def extract_classview(cls: web.View) -> web.View:
    for method_name in ("get", "post", "put", "patch", "delete"):
        handler = getattr(cls, method_name, None)
        if handler is None:
            continue
        patched = with_extraction(handler, classview=True)
        setattr(cls, method_name, patched)
    return cls
