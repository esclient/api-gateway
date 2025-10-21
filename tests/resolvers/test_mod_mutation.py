from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from faker import Faker
from graphql import GraphQLError

from apigateway.clients.base_client import GrpcError
from apigateway.resolvers.mutation.mod import (
    ModStatus,
    resolve_create_mod,
    resolve_set_status_mod,
)


def build_info(**clients: object) -> SimpleNamespace:
    return SimpleNamespace(context={"clients": clients})


@pytest.mark.asyncio
async def test_resolve_create_mod_returns_payload_dict(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    s3_key = f"{mod_id}/{faker.file_name()}"
    upload_url = faker.url()
    title = faker.sentence(nb_words=3)
    author_id = faker.random_int(min=1)
    filename = faker.file_name(extension="zip")
    description = faker.sentence(nb_words=6)
    client = SimpleNamespace(
        create_mod=AsyncMock(return_value=SimpleNamespace(mod_id=mod_id, s3_key=s3_key, upload_url=upload_url))
    )

    result = await resolve_create_mod(
        parent=None,
        info=build_info(mod_service=client),
        input={
            "title": title,
            "author_id": str(author_id),
            "filename": filename,
            "description": description,
        },
    )

    assert result == {"mod_id": mod_id, "s3_key": s3_key, "upload_url": upload_url}
    client.create_mod.assert_awaited_once_with(title, author_id, filename, description)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_resolve_set_status_mod_returns_success(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    client = SimpleNamespace(set_status_mod=AsyncMock(return_value=SimpleNamespace(success=True)))

    result = await resolve_set_status_mod(
        parent=None,
        info=build_info(mod_service=client),
        input={"mod_id": str(mod_id), "status": ModStatus.MOD_STATUS_BANNED},
    )

    assert result is True
    client.set_status_mod.assert_awaited_once_with(mod_id, ModStatus.MOD_STATUS_BANNED.value)  # type: ignore[attr-defined]


@pytest.mark.asyncio
async def test_mod_mutations_wrap_grpc_errors(faker: Faker) -> None:
    mod_id = faker.random_int(min=1)
    error_message = faker.sentence(nb_words=5)
    client = SimpleNamespace(set_status_mod=AsyncMock(side_effect=GrpcError(error_message)))

    with pytest.raises(GraphQLError) as exc:
        await resolve_set_status_mod(
            parent=None,
            info=build_info(mod_service=client),
            input={"mod_id": str(mod_id), "status": ModStatus.MOD_STATUS_HIDDEN},
        )

    assert "gRPC" in str(exc.value)
