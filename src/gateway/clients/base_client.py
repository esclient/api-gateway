import logging
from typing import Any, ClassVar, Self

import grpc
import grpc.aio
from google.protobuf import message as _message

from ..helpers.retry import grpc_retry

logger = logging.getLogger(__name__)


class GRPCError(Exception):
    pass


class RPCDoesNotExistException(GRPCError):
    """Исключение когда RPC метод не найден в gRPC стабе"""


class GRPCClient:
    _RPC_REQUEST_CLASSES: ClassVar[dict[str, type[_message.Message]]] = {}

    def __init__(self, channel: grpc.Channel):
        """
        Args:
            channel: gRPC канал для соединения
        """
        self._channel = channel
        self._stub = None
        self._initialize_stub()

    def _initialize_stub(self) -> None:
        """Инициализация стаба"""
        raise NotImplementedError()

    @grpc_retry()  # type: ignore
    def call_rpc(self, rpc_name: str, request_data: dict[str, Any], timeout: int = 30) -> _message.Message:
        """
        Универсальный метод вызова RPC

        Args:
            rpc_name: имя RPC метода
            request_data: данные для запроса
            timeout: таймаут в секундах

        Returns:
            gRPC response message
        """
        try:
            rpc_method = self._get_rpc_method(rpc_name)

            request = self._create_request(rpc_name, request_data)

            logger.debug(f"Вызов gRPC: {rpc_name} Данные: {request_data}")
            response: _message.Message = rpc_method(request, timeout=timeout)  # type: ignore[operator]

            return response

        except grpc.RpcError as e:
            logger.error(f"gRPC ошибка {rpc_name}: {e}")
            raise GRPCError(f"gRPC Ошибка вызова: {e}") from e
        except Exception as e:
            logger.error(f"Неизвестная ошибка при вызове {rpc_name}: {e}")
            raise

    def _get_rpc_method(self, rpc_name: str) -> _message.Message:
        """Получаем RPC метод из стаба"""
        rpc_method: _message.Message = getattr(self._stub, rpc_name, None)  # type: ignore[assignment]
        if rpc_method is None:
            raise RPCDoesNotExistException(f"RPC метод '{rpc_name}' не найден в стабе")
        return rpc_method

    def _create_request(self, rpc_name: str, request_data: dict[str, Any]) -> _message.Message:
        """
        Создает gRPC request message из словаря
        """
        raise NotImplementedError()

    def close(self) -> None:
        """Закрывает соединение"""
        if self._channel:
            self._channel.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        self.close()


class AsyncGRPCClient:
    _RPC_REQUEST_CLASSES: ClassVar[dict[str, type[_message.Message]]] = {}

    def __init__(self, channel: grpc.aio.Channel):
        self._channel = channel
        self._stub = None
        self._initialize_stub()

    def _initialize_stub(self) -> None:
        raise NotImplementedError()

    @grpc_retry()  # type: ignore
    async def call_rpc(self, rpc_name: str, request_data: dict[str, Any], timeout: int = 30) -> _message.Message:
        """
        Универсальный метод вызова RPC (async)

        Args:
            rpc_name: имя RPC метода
            request_data: данные для запроса
            timeout: таймаут в секундах

        Returns:
            gRPC response message
        """
        try:
            rpc_method = self._get_rpc_method(rpc_name)
            request = self._create_request(rpc_name, request_data)

            response: _message.Message = await rpc_method(request, timeout=timeout)  # type: ignore[operator]
            return response

        except grpc.RpcError as e:
            logger.error(f"gRPC ошибка {rpc_name}: {e} (async)")
            raise GRPCError(f"gRPC Ошибка вызова: {e} (async)") from e
        except Exception as e:
            logger.error(f"Неизвестная ошибка при вызове {rpc_name}: {e} (async)")
            raise

    def _get_rpc_method(self, rpc_name: str) -> _message.Message:
        rpc_method: _message.Message | None = getattr(self._stub, rpc_name, None)
        if not rpc_method:
            raise RPCDoesNotExistException(f"RPC метод '{rpc_name}' не найден в стабе (async)")
        return rpc_method

    def _create_request(self, rpc_name: str, request_data: dict[str, Any]) -> _message.Message:
        raise NotImplementedError()

    async def close(self) -> None:
        if self._channel:
            await self._channel.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        await self.close()
