from abc import ABCMeta
from typing import Any, Dict, Iterable, Union


class ParameterMeta(ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __getitem__(cls, key: Union[str, type, Iterable]) -> "type":
        default_attrs: Dict[str, Any] = {"name": None, "type": None}
        default_attrs.update(cls.__parse_key__(key))

        return type(cls.__name__, (cls,), default_attrs)
