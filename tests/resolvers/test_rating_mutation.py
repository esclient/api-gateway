from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from graphql import GraphQLError

from apigateway.clients.base_client import GrpcError
from apigateway.resolvers.mutation.rating import RateType, resolve_add_rate


def build_info(**clients: object) -> SimpleNamespace:
    return SimpleNamespace(context={"clients": clients})


@pytest.mark.asyncio
async def test_resolve_add_rate_returns_rate_id(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    author_id = faker.random_int(min=1)
    rate_id = faker.random_int(min=1)
    client = SimpleNamespace(rate_mod=AsyncMock(return_value=SimpleNamespace(rate_id=rate_id)))

    result = await resolve_add_rate(
        parent=None,
        info=build_info(rating_service=client),
        input={"mod_id": str(mod_id), "author_id": str(author_id), "rate": RateType.RATE_5},
    )

    assert result == str(rate_id)
    client.rate_mod.assert_awaited_once_with(mod_id, author_id, RateType.RATE_5.value)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_rating_mutation_wraps_grpc_errors(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    author_id = faker.random_int(min=1)
    error_message = faker.sentence(nb_words=4)
    client = SimpleNamespace(rate_mod=AsyncMock(side_effect=GrpcError(error_message)))

    with pytest.raises(GraphQLError) as exc:
        await resolve_add_rate(
            parent=None,
            info=build_info(rating_service=client),
            input={"mod_id": str(mod_id), "author_id": str(author_id), "rate": RateType.RATE_1},
        )

    assert "gRPC" in str(exc.value)
