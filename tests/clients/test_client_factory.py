from collections.abc import Callable
from typing import Any
from unittest.mock import AsyncMock

import pytest
from faker import Faker

from apigateway.clients.client_factory import GrpcClientFactory


class _StubChannel:
    def __init__(self) -> None:
        self.closed = False

    def unary_unary(self, *_: Any, **__: Any) -> Callable[..., Any]:
        async_mock = AsyncMock()
        async_mock.__name__ = "unary_unary_mock"
        return async_mock

    async def close(self) -> None:
        self.closed = True


@pytest.fixture
def stub_channel_factory(monkeypatch: pytest.MonkeyPatch):
    created_channels: list[_StubChannel] = []

    def _factory(_: str) -> _StubChannel:
        channel = _StubChannel()
        created_channels.append(channel)
        return channel

    monkeypatch.setattr(
        "apigateway.clients.client_factory.grpc.aio.insecure_channel",
        _factory,
    )
    return created_channels


def test_factory_reuses_channel_instances(stub_channel_factory: list[_StubChannel], faker: Faker) -> None:
    comment_endpoint = f"{faker.hostname()}:{faker.port_number()}"
    mod_endpoint = f"{faker.hostname()}:{faker.port_number()}"
    rating_endpoint = f"{faker.hostname()}:{faker.port_number()}"
    factory = GrpcClientFactory(comment_endpoint, mod_endpoint, rating_endpoint)

    comment_client_first = factory.get_comment_client()
    comment_client_second = factory.get_comment_client()

    assert comment_client_first is not comment_client_second
    assert comment_client_first._channel is comment_client_second._channel  # type: ignore[attr-defined]
    assert len(stub_channel_factory) == 1


@pytest.mark.asyncio
async def test_close_all_closes_each_channel(stub_channel_factory: list[_StubChannel], faker: Faker) -> None:
    comment_endpoint = f"{faker.hostname()}:{faker.port_number()}"
    mod_endpoint = f"{faker.hostname()}:{faker.port_number()}"
    rating_endpoint = f"{faker.hostname()}:{faker.port_number()}"
    factory = GrpcClientFactory(comment_endpoint, mod_endpoint, rating_endpoint)

    factory.get_comment_client()
    factory.get_mod_client()
    factory.get_rating_client()

    await factory.close_all()

    assert len(stub_channel_factory) == 3
    assert all(channel.closed for channel in stub_channel_factory)
