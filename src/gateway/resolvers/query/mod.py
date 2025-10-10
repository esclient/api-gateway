from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from gateway.converters.mod_status_converter import proto_to_graphql_mod_status
from gateway.helpers.id_helper import validate_and_convert_id


class GetModDownloadLinkInput(BaseModel):
    mod_id: int

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")


mod_query = ObjectType("ModQuery")


@mod_query.field("getModDownloadLink")
def resolve_get_mod_download_link(parent: object, info: GraphQLResolveInfo, input: GetModDownloadLinkInput) -> str:
    data = GetModDownloadLinkInput.model_validate(input)
    client = info.context["clients"]["mod_service"]
    resp = client.get_mod_download_link(data.mod_id)
    return resp.link_url


@mod_query.field("getMods")
def resolve_get_mods(parent: object, info: GraphQLResolveInfo) -> list[dict[str, Any]]:
    client = info.context["clients"]["mod_service"]
    resp = client.get_mods()
    return [
        {
            "id": item.id,
            "author_id": item.author_id,
            "title": item.title,
            "description": item.description,
            "version": item.version,
            "status": proto_to_graphql_mod_status(item.status),
            "created_at": int(item.created_at.seconds),
        }
        for item in resp.mods
    ]
