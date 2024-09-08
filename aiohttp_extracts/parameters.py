from __future__ import annotations

from abc import ABC, ABCMeta, abstractmethod
from token import OP
from typing import Any, Dict, Iterable, Optional, Type, Union

from aiohttp import web
from multidict import MultiMapping


class ParameterMeta(ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: Union[str, type, Iterable]) -> Dict[str, Any]:
        return self.__parse_key__(key)

    @staticmethod
    def __parse_key__(key: Union[str, type, Iterable]) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        if isinstance(key, str):
            params["name"] = key
        elif isinstance(key, type):
            params["type"] = key
        elif isinstance(key, Iterable):
            params.update({k: v for k, v in zip(("name", "type"), key)})
        return params


class Parameter(ABC, metaclass=ParameterMeta):
    name: Optional[str]
    type: Optional[Type]

    def __init__(self, name: Optional[str] = None, type: Optional[Type] = None) -> None:
        self.name = name
        self.type = type

    @classmethod
    @abstractmethod
    async def extract(cls, name: str, request: web.Request) -> Any:
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


class Header(Parameter):

    @classmethod
    async def extract(cls, name: str, request: web.Request) -> Optional[str]:
        if cls.name:
            name = cls.name
        name = (
            name.capitalize()
            if len(name) == 1
            else "-".join(word.capitalize() for word in name.split("_"))
        )
        return request.headers.get(name)


class Cookie(Parameter):
    @classmethod
    async def extract(cls, name: str, request: web.Request) -> Optional[str]:
        name = cls.name or name
        return request.cookies.get(name)


class JSONBody(Parameter):
    @classmethod
    async def extract(cls, name: str, request: web.Request) -> Any:
        return await request.json()


class MatchInfo(Parameter):
    @classmethod
    async def extract(cls, name: str, request: web.Request) -> Optional[str]:
        name = cls.name or name
        return request.match_info.get(name)


class Query(Parameter):

    @classmethod
    async def extract(cls, name: str, request: web.Request) -> Any:
        name = cls.name or name
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


class RequestAttr(Parameter):
    name: Optional[str] = None

    @classmethod
    async def extract(cls, name: str, request: web.Request) -> Any:
        name = cls.name or name
        return request.get(name, None)


class File(Parameter):
    def __init__(
        self, name: str, filename: str, content: bytes, headers: MultiMapping[str]
    ):
        self.name = name
        self.filename = filename
        self.content = content
        self.headers = headers

    @classmethod
    async def extract(cls, request: web.Request, name: str) -> Optional[File]:
        if cls.name:
            name = cls.name
        reader = await request.multipart()

        async for part in reader:
            if part.name == name:  # type: ignore
                filename = part.filename  # type: ignore
                content = await part.read(decode=True)  # type: ignore
                headers = part.headers  # type: ignore

                return cls(
                    name=name, filename=filename, content=content, headers=headers  # type: ignore
                )

        return None