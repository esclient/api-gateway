import grpc
import grpc.aio
import logging
from typing import Dict, Any
from google.protobuf import message as _message


logger = logging.getLogger(__name__)

class GRPCError(Exception): ...

class RPCDoesNotExistException(GRPCError):
    """Исключение когда RPC метод не найден в gRPC стабе"""

class GRPCClient:
    _RPC_REQUEST_CLASSES = { }

    def __init__(self, channel: grpc.Channel):
        """
        Args:
            channel: gRPC канал для соединения
        """
        self._channel = channel
        self._stub = None
        self._initialize_stub()

    def _initialize_stub(self):
        """Инициализация стаба"""
        raise NotImplementedError()

    def call_rpc(self, rpc_name: str, request_data: Dict[str, Any], timeout: int = 30) -> _message.Message:
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
            response = rpc_method(request, timeout=timeout)
            
            return response
            
        except grpc.RpcError as e:
            logger.error(f"gRPC ошибка {rpc_name}: {e}")
            raise GRPCError(f"gRPC Ошибка вызова: {e}") from e
        except Exception as e:
            logger.error(f"Неизвестная ошибка при вызове {rpc_name}: {e}")
            raise
    
    def _get_rpc_method(self, rpc_name: str):
        """Получаем RPC метод из стаба"""
        rpc_method = getattr(self._stub, rpc_name, None)
        if rpc_method is None:
            raise RPCDoesNotExistException(f"RPC метод '{rpc_name}' не найден в стабе")
        return rpc_method
    
    def _create_request(self, rpc_name: str, request_data: Dict[str, Any]) -> _message.Message:
        """
        Создает gRPC request message из словаря
        """
        raise NotImplementedError()
    
    def close(self):
        """Закрывает соединение"""
        if self._channel:
            self._channel.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class AsyncGRPCClient:
    def __init__(self, channel: grpc.aio.Channel):
        self._channel = channel
        self._stub = None
        self._initialize_stub()

    def _initialize_stub(self):
        raise NotImplementedError()
    
    async def call_rpc(self, rpc_name: str, request_data: Dict[str, Any], timeout: int = 30) -> _message.Message:
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
            
            response = await rpc_method(request, timeout=timeout)
            return response
            
        except grpc.RpcError as e:
            logger.error(f"gRPC ошибка {rpc_name}: {e} (async)")
            raise GRPCError(f"gRPC Ошибка вызова: {e} (async)") from e
        except Exception as e:
            logger.error(f"Неизвестная ошибка при вызове {rpc_name}: {e} (async)")
            raise
    
    def _get_rpc_method(self, rpc_name: str):
        rpc_method = getattr(self._stub, rpc_name, None)
        if not rpc_method:
            raise RPCDoesNotExistException(f"RPC метод '{rpc_name}' не найден в стабе (async)")
        return rpc_method
    
    def _create_request(self, rpc_name: str, request_data: Dict[str, Any]) -> _message.Message:
        raise NotImplementedError()
    
    async def close(self):
        if self._channel:
            await self._channel.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
