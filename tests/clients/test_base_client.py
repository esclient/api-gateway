import asyncio
from types import SimpleNamespace
from typing import Any, cast

import grpc
import grpc.aio
import pytest
from faker import Faker
from google.protobuf import message as _message

from apigateway.clients.base_client import GrpcClient, GrpcError


class _FakeChannel:
    def __init__(self) -> None:
        self.closed = False

    async def close(self) -> None:
        self.closed = True


class _FakeRpcError(grpc.RpcError):
    def __init__(self, status_code: grpc.StatusCode) -> None:
        super().__init__()
        self._status_code = status_code

    def code(self) -> grpc.StatusCode:  # type: ignore[override]
        return self._status_code


class _ConcreteClient(GrpcClient[SimpleNamespace]):
    def __init__(self, channel: _FakeChannel) -> None:
        self.stub_initialized = False
        super().__init__(cast(grpc.aio.Channel, channel))

    def _initialize_stub(self) -> SimpleNamespace:
        self.stub_initialized = True
        return SimpleNamespace()


@pytest.mark.asyncio
async def test_call_invokes_rpc_method_with_timeout(faker: Faker) -> None:
    channel = _FakeChannel()
    client = _ConcreteClient(channel)
    captured: dict[str, Any] = {}
    request_payload = cast(_message.Message, SimpleNamespace(payload=faker.pystr()))
    expected_response = faker.pystr()
    timeout_value = faker.random_int(min=1, max=60)

    async def rpc_method(request: _message.Message, timeout: int = 30) -> str:
        await asyncio.sleep(0)
        captured["request"] = request
        captured["timeout"] = timeout
        return expected_response

    result = await client.call(rpc_method, request=request_payload, timeout=timeout_value)

    assert result == expected_response
    assert captured == {"request": request_payload, "timeout": timeout_value}


@pytest.mark.asyncio
async def test_call_wraps_grpc_errors() -> None:
    channel = _FakeChannel()
    client = _ConcreteClient(channel)

    async def failing_rpc(request: _message.Message, timeout: int = 30) -> str:
        await asyncio.sleep(0)
        raise _FakeRpcError(grpc.StatusCode.INVALID_ARGUMENT)

    with pytest.raises(GrpcError) as exc:
        await client.call(failing_rpc, request=cast(_message.Message, SimpleNamespace()))

    assert "gRPC" in str(exc.value)


@pytest.mark.asyncio
async def test_call_propagates_other_exceptions(faker: Faker) -> None:
    channel = _FakeChannel()
    client = _ConcreteClient(channel)
    error_message = faker.sentence(nb_words=3)

    async def failing_rpc(request: _message.Message, timeout: int = 30) -> str:
        await asyncio.sleep(0)
        raise RuntimeError(error_message)

    with pytest.raises(RuntimeError) as exc:
        await client.call(failing_rpc, request=cast(_message.Message, SimpleNamespace()))

    assert str(exc.value) == error_message


@pytest.mark.asyncio
async def test_close_closes_channel() -> None:
    channel = _FakeChannel()
    client = _ConcreteClient(channel)

    await client.close()

    assert channel.closed is True
