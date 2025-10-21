from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from graphql import GraphQLError

from apigateway.clients.base_client import GrpcError
from apigateway.resolvers.mutation.comment import (
    resolve_create_comment,
    resolve_delete_comment,
    resolve_edit_comment,
)


def build_info(**clients: object) -> SimpleNamespace:
    return SimpleNamespace(context={"clients": clients})


@pytest.mark.asyncio
async def test_resolve_create_comment_returns_new_id(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    author_id = faker.random_int(min=1)
    comment_id = faker.random_int(min=1)
    comment_text = faker.sentence(nb_words=5)
    client = SimpleNamespace(create_comment=AsyncMock(return_value=SimpleNamespace(comment_id=comment_id)))

    result = await resolve_create_comment(
        parent=None,
        info=build_info(comment_service=client),
        input={"mod_id": str(mod_id), "author_id": str(author_id), "text": comment_text},
    )

    assert result == str(comment_id)
    client.create_comment.assert_awaited_once_with(mod_id, author_id, comment_text)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_resolve_edit_comment_returns_success_flag(faker: Faker) -> None:
    comment_id = faker.random_int(min=1)
    new_text = faker.sentence(nb_words=4)
    client = SimpleNamespace(edit_comment=AsyncMock(return_value=SimpleNamespace(success=True)))

    result = await resolve_edit_comment(
        parent=None,
        info=build_info(comment_service=client),
        input={"comment_id": str(comment_id), "text": new_text},
    )

    assert result is True
    client.edit_comment.assert_awaited_once_with(comment_id, new_text)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_resolve_delete_comment_returns_success_flag(faker: Faker) -> None:
    comment_id = faker.random_int(min=1)
    client = SimpleNamespace(delete_comment=AsyncMock(return_value=SimpleNamespace(success=True)))

    result = await resolve_delete_comment(
        parent=None,
        info=build_info(comment_service=client),
        input={"comment_id": str(comment_id)},
    )

    assert result is True
    client.delete_comment.assert_awaited_once_with(comment_id)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_comment_mutations_wrap_grpc_errors(faker: Faker) -> None:
    comment_id = faker.random_int(min=1)
    error_message = faker.sentence(nb_words=6)
    client = SimpleNamespace(
        delete_comment=AsyncMock(side_effect=GrpcError(error_message)),
    )

    with pytest.raises(GraphQLError) as exc:
        await resolve_delete_comment(
            parent=None,
            info=build_info(comment_service=client),
            input={"comment_id": str(comment_id)},
        )

    assert "gRPC" in str(exc.value)
