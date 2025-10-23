from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoginUserRequest(_message.Message):
    __slots__ = ("username_or_email", "password")
    USERNAME_OR_EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    username_or_email: str
    password: str
    def __init__(self, username_or_email: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class RegisterUserRequest(_message.Message):
    __slots__ = ("login", "email", "password", "confirm_password")
    LOGIN_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    login: str
    email: str
    password: str
    confirm_password: str
    def __init__(self, login: _Optional[str] = ..., email: _Optional[str] = ..., password: _Optional[str] = ..., confirm_password: _Optional[str] = ...) -> None: ...

class VerifyUserRequest(_message.Message):
    __slots__ = ("user_id", "confirmation_code")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    CONFIRMATION_CODE_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    confirmation_code: str
    def __init__(self, user_id: _Optional[int] = ..., confirmation_code: _Optional[str] = ...) -> None: ...

class LoginUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class RegisterUserResponse(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    def __init__(self, user_id: _Optional[int] = ...) -> None: ...

class VerifyUserResponse(_message.Message):
    __slots__ = ("is_verified",)
    IS_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    is_verified: bool
    def __init__(self, is_verified: bool = ...) -> None: ...
