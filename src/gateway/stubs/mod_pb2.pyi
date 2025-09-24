from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

DESCRIPTOR: _descriptor.FileDescriptor

class ModStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MOD_STATUS_UNSPECIFIED: _ClassVar[ModStatus]
    MOD_STATUS_UPLOADED: _ClassVar[ModStatus]
    MOD_STATUS_BANNED: _ClassVar[ModStatus]
    MOD_STATUS_HIDDEN: _ClassVar[ModStatus]

MOD_STATUS_UNSPECIFIED: ModStatus
MOD_STATUS_UPLOADED: ModStatus
MOD_STATUS_BANNED: ModStatus
MOD_STATUS_HIDDEN: ModStatus

class SetStatusRequest(_message.Message):
    __slots__ = ("mod_id", "status")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    status: ModStatus
    def __init__(
        self,
        mod_id: int | None = ...,
        status: ModStatus | str | None = ...,
    ) -> None: ...

class SetStatusResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CreateModRequest(_message.Message):
    __slots__ = ("author_id", "description", "filename", "mod_title")
    MOD_TITLE_FIELD_NUMBER: _ClassVar[int]
    AUTHOR_ID_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    mod_title: str
    author_id: int
    filename: str
    description: str
    def __init__(
        self,
        mod_title: str | None = ...,
        author_id: int | None = ...,
        filename: str | None = ...,
        description: str | None = ...,
    ) -> None: ...

class CreateModResponse(_message.Message):
    __slots__ = ("mod_id", "s3_key", "upload_url")
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_URL_FIELD_NUMBER: _ClassVar[int]
    S3_KEY_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    upload_url: str
    s3_key: str
    def __init__(
        self,
        mod_id: int | None = ...,
        upload_url: str | None = ...,
        s3_key: str | None = ...,
    ) -> None: ...

class ConfirmUploadRequest(_message.Message):
    __slots__ = ("mod_id",)
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    def __init__(self, mod_id: int | None = ...) -> None: ...

class GetModDownloadLinkRequest(_message.Message):
    __slots__ = ("mod_id",)
    MOD_ID_FIELD_NUMBER: _ClassVar[int]
    mod_id: int
    def __init__(self, mod_id: int | None = ...) -> None: ...

class GetModDownloadLinkResponse(_message.Message):
    __slots__ = ("link_url",)
    LINK_URL_FIELD_NUMBER: _ClassVar[int]
    link_url: str
    def __init__(self, link_url: str | None = ...) -> None: ...
