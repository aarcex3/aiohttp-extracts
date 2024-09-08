import inspect
from functools import wraps
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Type, Union

from aiohttp import web

from .parameters import Parameter

AsyncFunc = Callable[..., Awaitable[web.Response]]
FunctionParams = Dict[str, Tuple[Union[web.Request, Parameter, type], Optional[Any]]]


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
        if not issubclass(annotation, (Parameter, web.Request)):
            raise TypeError(
                "{} type hints must be subclass of {}" "which {} is not".format(
                    fn.__name__, Parameter, annotation
                )
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
        for name, (type, default) in fn_params.items():
            if issubclass(type, web.Request):  # type: ignore
                params[name] = request
            else:
                params[name] = await type.extract(name, request) or default  # type: ignore
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
