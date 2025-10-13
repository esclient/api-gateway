import logging
from typing import Self
from collections.abc import Awaitable, Callable

import grpc
import grpc.aio
from google.protobuf import message as _message

from ..helpers.retry import grpc_retry

logger = logging.getLogger(__name__)


class GrpcError(Exception):
    pass


class GrpcClient:
    def __init__(self, channel: grpc.aio.Channel):
        self._channel = channel
        self._stub = None
        self._initialize_stub()

    def _initialize_stub(self) -> None:
        raise NotImplementedError()

    @grpc_retry()  # type: ignore
    async def call(
        self,
        rpc_method: Callable[["_message.Message"], Awaitable["_message.Message"]],
        request: "_message.Message",
        *,
        timeout: int = 30,
    ) -> "_message.Message":
        try:
            response: _message.Message = await rpc_method(request, timeout=timeout)  # type: ignore[operator]
            return response
        except grpc.RpcError as e:
            logger.error(f"gRPC ошибка {rpc_method.__name__ if hasattr(rpc_method, '__name__') else rpc_method}: {e}")
            raise GrpcError(f"gRPC Ошибка вызова: {e}") from e
        except Exception as e:
            logger.error(
                f"Неизвестная ошибка при вызове {rpc_method.__name__ if hasattr(rpc_method, '__name__') else rpc_method}: {e}"
            )
            raise

    async def close(self) -> None:
        if self._channel:
            await self._channel.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        await self.close()
