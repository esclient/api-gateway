import logging
from collections.abc import Awaitable, Callable
from types import TracebackType
from typing import Self, TypeVar

import grpc
import grpc.aio
from google.protobuf import message as _message

from apigateway.helpers.retry import grpc_retry

logger = logging.getLogger(__name__)

ResponseT = TypeVar("ResponseT", bound=_message.Message)


class GrpcError(Exception):
    pass


class GrpcClient[StubT]:
    def __init__(self, channel: grpc.aio.Channel):
        self._channel = channel
        self._stub: StubT = self._initialize_stub()

    def _initialize_stub(self) -> StubT:
        raise NotImplementedError

    @grpc_retry()
    async def call(
        self,
        rpc_method: Callable[..., Awaitable[ResponseT]],
        request: _message.Message,
        *,
        timeout: int = 30,
    ) -> ResponseT:
        method_name = getattr(rpc_method, "__name__", repr(rpc_method))

        try:
            response = await rpc_method(request, timeout=timeout)
            return response
        except grpc.RpcError as exc:
            logger.error("gRPC error while calling %s: %s", method_name, exc)
            raise GrpcError(f"gRPC call failed: {exc}") from exc
        except Exception as exc:
            logger.error("Unknown error while calling %s: %s", method_name, exc)
            raise

    async def close(self) -> None:
        await self._channel.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()
