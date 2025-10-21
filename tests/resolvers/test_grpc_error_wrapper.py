import asyncio

import pytest
from faker import Faker
from graphql import GraphQLError

from apigateway.clients.base_client import GrpcError
from apigateway.resolvers.grpc_error_wrapper import handle_grpc_errors


@pytest.mark.asyncio
async def test_async_wrapper_transforms_grpc_error(faker: Faker) -> None:
    error_message = faker.sentence(nb_words=3)

    @handle_grpc_errors
    async def failing() -> None:
        await asyncio.sleep(0)
        raise GrpcError(error_message)

    with pytest.raises(GraphQLError) as exc:
        await failing()

    assert "gRPC" in str(exc.value)


@pytest.mark.asyncio
async def test_async_wrapper_transforms_unknown_error(faker: Faker) -> None:
    error_message = faker.sentence(nb_words=3)

    @handle_grpc_errors
    async def failing() -> None:
        await asyncio.sleep(0)
        raise RuntimeError(error_message)

    with pytest.raises(GraphQLError) as exc:
        await failing()

    assert error_message in str(exc.value)


def test_sync_wrapper_transforms_grpc_error(faker: Faker) -> None:
    error_message = faker.sentence(nb_words=3)

    @handle_grpc_errors
    def failing() -> None:
        raise GrpcError(error_message)

    with pytest.raises(GraphQLError) as exc:
        failing()

    assert "gRPC" in str(exc.value)
