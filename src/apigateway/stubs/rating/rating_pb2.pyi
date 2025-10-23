from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

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
    __slots__ = ("mod_id", "author_id", "rate")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    author_id: int
    rate: Rate
    def __init__(self, mod_id: _Optional[int] = ..., author_id: _Optional[int] = ..., rate: _Optional[_Union[Rate, str]] = ...) -> None: ...

class RateModResponse(_message.Message):
    __slots__ = ("rate_id",)
    RATE_ID_FIELD_NUMBER: _ClassVar[int]
    rate_id: int
    def __init__(self, rate_id: _Optional[int] = ...) -> None: ...

class GetRatesRequest(_message.Message):
    __slots__ = ("mod_id",)
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    def __init__(self, mod_id: _Optional[int] = ...) -> None: ...

class GetRatesResponse(_message.Message):
    __slots__ = ("rates_total", "rate_1", "rate_2", "rate_3", "rate_4", "rate_5")
    RATES_TOTAL_FIELD_NUMBER: _ClassVar[int]
    RATE_1_FIELD_NUMBER: _ClassVar[int]
    RATE_2_FIELD_NUMBER: _ClassVar[int]
    RATE_3_FIELD_NUMBER: _ClassVar[int]
    RATE_4_FIELD_NUMBER: _ClassVar[int]
    RATE_5_FIELD_NUMBER: _ClassVar[int]
    rates_total: int
    rate_1: int
    rate_2: int
    rate_3: int
    rate_4: int
    rate_5: int
    def __init__(self, rates_total: _Optional[int] = ..., rate_1: _Optional[int] = ..., rate_2: _Optional[int] = ..., rate_3: _Optional[int] = ..., rate_4: _Optional[int] = ..., rate_5: _Optional[int] = ...) -> None: ...
