from datetime import datetime
from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from apigateway.converters.mod_status_converter import proto_to_graphql_mod_status
from apigateway.helpers.datetime_helper import timestamp_to_datetime
from apigateway.helpers.id_helper import validate_and_convert_id
from apigateway.resolvers.grpc_error_wrapper import handle_grpc_errors

mod_query = ObjectType("ModQuery")


class GetModDownloadLinkInput(BaseModel):
    mod_id: int

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")


@mod_query.field("getModDownloadLink")
@handle_grpc_errors
async def resolve_get_mod_download_link(
    parent: object, info: GraphQLResolveInfo, input: GetModDownloadLinkInput
) -> str:
    data = GetModDownloadLinkInput.model_validate(input)
    client = info.context["clients"]["mod_service"]
    resp = await client.get_mod_download_link(data.mod_id)
    return resp.link_url  # type: ignore


class GetModsResult(BaseModel):
    id: int
    author_id: int
    title: str
    description: str
    version: str
    status: str
    created_at: datetime

    @field_validator("created_at", mode="before")
    def _created_at(cls, value: Any) -> datetime:
        return timestamp_to_datetime(value)


@mod_query.field("getMods")
@handle_grpc_errors
async def resolve_get_mods(parent: object, info: GraphQLResolveInfo) -> list[dict[str, Any]]:
    client = info.context["clients"]["mod_service"]
    resp = await client.get_mods()
    return [
        GetModsResult(
            id=item.id,
            author_id=item.author_id,
            title=item.title,
            description=item.description,
            version=item.version,
            status=proto_to_graphql_mod_status(item.status),
            created_at=item.created_at,
        ).model_dump()
        for item in resp.mods
    ]
