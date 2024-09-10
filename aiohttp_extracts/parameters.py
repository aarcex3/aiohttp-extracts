from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict, Generic, Iterable, Mapping, Optional, Type, TypeVar, Union

from aiohttp import BodyPartReader, MultipartReader, web
from aiohttp.web_exceptions import HTTPException
from multidict import CIMultiDictProxy

from aiohttp_extracts.meta import ParameterMeta

T = TypeVar("T")


class Parameter(ABC, Generic[T], metaclass=ParameterMeta):
    name: Optional[str]
    type: Optional[Type[T]]

    def __init__(
        self, name: Optional[str] = None, type: Optional[Type[T]] = None
    ) -> None:
        self.name = name
        self.type = type

    @classmethod
    @abstractmethod
    async def extract(cls, request: web.Request, name: Optional[str] = None) -> T:
        """
        Abstract class method to extract data from a request.
        This method should be implemented by subclasses.
        """
        pass

    @staticmethod
    def __parse_key(key: Union[str, type, Iterable]) -> Dict[str, Any]:
        """
        Parses the key to determine the name and type attributes.
        This is a static method as it doesn't rely on instance or class-level data.
        """
        params: Dict[str, Any] = {}
        if isinstance(key, str):
            params["name"] = key
        elif isinstance(key, type):
            params["type"] = key
        elif isinstance(key, Iterable):
            params.update({k: v for k, v in zip(("name", "type"), key)})
        return params

    def __repr__(self) -> str:
        return "{}(name: {}, type: {})".format(
            self.__class__.__name__, self.name, self.type
        )


class Header(Parameter[str]):
    @classmethod
    async def extract(cls, request: web.Request, name: Optional[str] = None) -> str:
        name = (
            name.capitalize()
            if len(name) == 1
            else "-".join(word.capitalize() for word in name.split("_"))
        )
        value = request.headers.get(name)
        if value is None:
            raise web.HTTPBadRequest(reason=f"Missing header '{name}'.")
        return value


class Cookie(Parameter[str]):
    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Optional[str]:
        return request.cookies.get(name)


class ReqBody(Parameter[Dict[str, Any]]):
    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Dict[str, Any]:
        if request.can_read_body:
            return await request.json()
        else:
            raise web.HTTPBadRequest(reason="Request body is missing.")


class Path(Parameter[str]):
    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Optional[str]:
        value = request.match_info.get(name)

        if value is None:
            raise web.HTTPBadRequest(reason=f"Missing query parameter '{name}'.")
        if cls.type:
            try:
                return cls.type(value)
            except (ValueError, TypeError):
                raise web.HTTPBadRequest(
                    reason=f"Invalid type for query parameter '{name}'. Expected {cls.type.__name__}."
                )

        return value


class Query(Parameter[str]):
    @classmethod
    async def extract(cls, request: web.Request, name: Optional[str] = None) -> T:
        value = request.query.get(name)

        if value is None:
            raise web.HTTPBadRequest(reason=f"Missing query parameter '{name}'.")
        if cls.type:
            try:
                return cls.type(value)
            except (ValueError, TypeError):
                raise web.HTTPBadRequest(
                    reason=f"Invalid type for query parameter '{name}'. Expected {cls.type.__name__}."
                )

        return value


class RequestAttr(Parameter[Any]):
    name: Optional[str] = None

    @classmethod
    async def extract(cls, request: web.Request, name: Optional[str] = None) -> Any:
        if cls.name:
            name = cls.name
        return request.get(name, None)


class File(Parameter[bytes]):
    def __init__(
        self,
        name: str,
        filename: Optional[str],
        content: bytes,
        headers: Union[Mapping[str, str], CIMultiDictProxy[str]],
    ):
        super().__init__(name=name, type=bytes)
        self.filename = filename
        self.content = content
        self.headers = headers

    @classmethod
    async def extract(
        cls, request: web.Request, name: Optional[str] = None
    ) -> Optional["File"]:
        try:
            if cls.name:
                name = cls.name

            reader: MultipartReader = await request.multipart()

            async for part in reader:
                if isinstance(part, BodyPartReader):
                    if getattr(part, "name", None) == name:
                        filename = getattr(part, "filename", None)
                        content = await part.read(decode=True)
                        headers = getattr(part, "headers", {})

                        return cls(
                            name=name,
                            filename=filename,
                            content=content,
                            headers=headers,
                        )
        except Exception as e:
            raise HTTPException(text=f"{e}") from e

        return None
