import asyncio
from collections.abc import Callable
from functools import wraps
from typing import Any

from graphql import GraphQLError

from ..clients.base_client import GrpcError


def handle_grpc_errors(func: Callable) -> Callable:  # type: ignore
    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:  # type: ignore
            try:
                return await func(*args, **kwargs)
            except GrpcError as e:
                raise GraphQLError(f"gRPC ошибка: {e}") from None
            except Exception as e:
                raise GraphQLError(f"Неизвестная ошибка: {e}") from None

        return async_wrapper

    else:

        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:  # type: ignore
            try:
                return func(*args, **kwargs)
            except GrpcError as e:
                raise GraphQLError(f"gRPC ошибка: {e}") from None
            except Exception as e:
                raise GraphQLError(f"Неизвестная ошибка: {e}") from None

        return sync_wrapper
