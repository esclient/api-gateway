from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Comment(_message.Message):
    __slots__ = ("author_id", "created_at", "edited_at", "id", "text")
    ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    EDITED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    author_id: int
    text: str
    created_at: int
    edited_at: int
    def __init__(
        self,
        id: int | None = ...,
        author_id: int | None = ...,
        text: str | None = ...,
        created_at: int | None = ...,
        edited_at: int | None = ...,
    ) -> None: ...

class CreateCommentRequest(_message.Message):
    __slots__ = ("author_id", "mod_id", "text")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    author_id: int
    text: str
    def __init__(
        self,
        mod_id: int | None = ...,
        author_id: int | None = ...,
        text: str | None = ...,
    ) -> None: ...

class CreateCommentResponse(_message.Message):
    __slots__ = ("comment_id",)
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    def __init__(self, comment_id: int | None = ...) -> None: ...

class GetCommentsRequest(_message.Message):
    __slots__ = ("mod_id",)
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    def __init__(self, mod_id: int | None = ...) -> None: ...

class GetCommentsResponse(_message.Message):
    __slots__ = ("comments", "mod_id")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    COMMENTS_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    comments: _containers.RepeatedCompositeFieldContainer[Comment]
    def __init__(
        self,
        mod_id: int | None = ...,
        comments: _Iterable[Comment | _Mapping] | None = ...,
    ) -> None: ...

class DeleteCommentRequest(_message.Message):
    __slots__ = ("comment_id",)
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    def __init__(self, comment_id: int | None = ...) -> None: ...

class DeleteCommentResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class EditCommentRequest(_message.Message):
    __slots__ = ("comment_id", "text")
    COMMENT_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    comment_id: int
    text: str
    def __init__(self, comment_id: int | None = ..., text: str | None = ...) -> None: ...

class EditCommentResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
