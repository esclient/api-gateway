from collections.abc import Callable
from functools import wraps
from typing import Any

from graphql import GraphQLError

from ..clients.base_client import GRPCError


def handle_grpc_errors(func: Callable) -> Callable:  # type: ignore
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:  # type: ignore
        try:
            return func(*args, **kwargs)
        except GRPCError as e:
            raise GraphQLError(f"gRPC ошибка: {e}") from None
        except Exception as e:
            raise GraphQLError(f"Неизвестная ошибка: {e}") from None

    return wrapper
