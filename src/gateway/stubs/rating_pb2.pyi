from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class Rate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RATE_UNSPECIFIED: _ClassVar[Rate]
    RATE_1: _ClassVar[Rate]
    RATE_2: _ClassVar[Rate]
    RATE_3: _ClassVar[Rate]
    RATE_4: _ClassVar[Rate]
    RATE_5: _ClassVar[Rate]

RATE_UNSPECIFIED: Rate
RATE_1: Rate
RATE_2: Rate
RATE_3: Rate
RATE_4: Rate
RATE_5: Rate

class RateModRequest(_message.Message):
    __slots__ = ("author_id", "mod_id", "rate")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    author_id: int
    rate: Rate
    def __init__(
        self,
        mod_id: int | None = ...,
        author_id: int | None = ...,
        rate: Rate | str | None = ...,
    ) -> None: ...

class RateModResponse(_message.Message):
    __slots__ = ("rate_id",)
    RATE_ID_FIELD_NUMBER: _ClassVar[int]
    rate_id: int
    def __init__(self, rate_id: int | None = ...) -> None: ...

class GetRatesRequest(_message.Message):
    __slots__ = ("mod_id",)
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    def __init__(self, mod_id: int | None = ...) -> None: ...

class GetRatesResponse(_message.Message):
    __slots__ = ("dislikes", "likes", "rates_total")
    RATES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    LIKES_FIELD_NUMBER: _ClassVar[int]
    DISLIKES_FIELD_NUMBER: _ClassVar[int]
    rates_total: int
    likes: int
    dislikes: int
    def __init__(
        self,
        rates_total: int | None = ...,
        likes: int | None = ...,
        dislikes: int | None = ...,
    ) -> None: ...
