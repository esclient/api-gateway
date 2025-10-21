from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from graphql import GraphQLError

from apigateway.clients.base_client import GrpcError
from apigateway.converters.mod_status_converter import PROTO_TO_GRAPHQL, proto_to_graphql_mod_status
from apigateway.resolvers.query.comment import resolve_get_comments
from apigateway.resolvers.query.mod import resolve_get_mod_download_link, resolve_get_mods


def build_info(**clients: object) -> SimpleNamespace:
    return SimpleNamespace(context={"clients": clients})


@pytest.mark.asyncio
async def test_resolve_get_mod_download_link_returns_url(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    link_url = faker.url()
    mod_client = SimpleNamespace(get_mod_download_link=AsyncMock(return_value=SimpleNamespace(link_url=link_url)))

    result = await resolve_get_mod_download_link(
        parent=None,
        info=build_info(mod_service=mod_client),
        input={"mod_id": str(mod_id)},
    )

    assert result == link_url
    mod_client.get_mod_download_link.assert_awaited_once_with(mod_id)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_resolve_get_mods_maps_proto_fields(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    author_id = faker.random_int(min=1)
    title = faker.sentence(nb_words=3)
    description = faker.sentence()
    version = faker.random_int(min=1, max=10)
    status = faker.random_element(list(PROTO_TO_GRAPHQL.keys()))
    created_at_seconds = faker.random_number(digits=6)
    mod_client = SimpleNamespace(
        get_mods=AsyncMock(
            return_value=SimpleNamespace(
                mods=[
                    SimpleNamespace(
                        id=mod_id,
                        author_id=author_id,
                        title=title,
                        description=description,
                        version=version,
                        status=status,
                        created_at=SimpleNamespace(seconds=created_at_seconds),
                    )
                ]
            )
        )
    )

    result = await resolve_get_mods(
        parent=None,
        info=build_info(mod_service=mod_client),
    )

    assert result == [
        {
            "id": mod_id,
            "author_id": author_id,
            "title": title,
            "description": description,
            "version": version,
            "status": proto_to_graphql_mod_status(status),
            "created_at": created_at_seconds,
        }
    ]


@pytest.mark.asyncio
async def test_resolve_get_comments_returns_serialized_comments(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    first_comment = SimpleNamespace(
        id=faker.random_int(min=1),
        text=faker.sentence(),
        author_id=faker.random_int(min=1),
        created_at=faker.random_int(min=1_000, max=9_999_999),
        edited_at=0,
    )
    second_comment = SimpleNamespace(
        id=faker.random_int(min=first_comment.id + 1, max=first_comment.id + 10_000),
        text=faker.sentence(),
        author_id=faker.random_int(min=1),
        created_at=faker.random_int(min=1_000, max=9_999_999),
        edited_at=faker.random_int(min=1, max=9_999_999),
    )
    comment_client = SimpleNamespace(
        get_comments=AsyncMock(return_value=SimpleNamespace(comments=[first_comment, second_comment]))
    )

    result = await resolve_get_comments(
        parent=None,
        info=build_info(comment_service=comment_client),
        input={"mod_id": str(mod_id)},
    )

    expected = [
        {
            "id": first_comment.id,
            "text": first_comment.text,
            "author_id": first_comment.author_id,
            "created_at": first_comment.created_at,
            "edited_at": None,
        },
        {
            "id": second_comment.id,
            "text": second_comment.text,
            "author_id": second_comment.author_id,
            "created_at": second_comment.created_at,
            "edited_at": second_comment.edited_at,
        },
    ]

    assert result == expected
    comment_client.get_comments.assert_awaited_once_with(mod_id)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_query_resolvers_wrap_grpc_errors(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    error_message = faker.sentence(nb_words=5)
    mod_client = SimpleNamespace(get_mod_download_link=AsyncMock(side_effect=GrpcError(error_message)))

    with pytest.raises(GraphQLError):
        await resolve_get_mod_download_link(
            parent=None,
            info=build_info(mod_service=mod_client),
            input={"mod_id": str(mod_id)},
        )
