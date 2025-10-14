from enum import StrEnum
from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from apigateway.helpers.id_helper import validate_and_convert_id

from ..grpc_error_wrapper import handle_grpc_errors

mod_mutation = ObjectType("ModMutation")


class ModStatus(StrEnum):
    MOD_STATUS_UNSPECIFIED = "MOD_STATUS_UNSPECIFIED"
    MOD_STATUS_UPLOADED = "MOD_STATUS_UPLOADED"
    MOD_STATUS_BANNED = "MOD_STATUS_BANNED"
    MOD_STATUS_HIDDEN = "MOD_STATUS_HIDDEN"


class CreateModInput(BaseModel):
    title: str
    author_id: int
    filename: str
    description: str

    @field_validator("author_id", mode="before")
    def validate_author_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "author_id")


class CreateModResult(BaseModel):
    mod_id: int
    s3_key: str
    upload_url: str


@mod_mutation.field("createMod")
@handle_grpc_errors
async def resolve_create_mod(parent: object, info: GraphQLResolveInfo, input: CreateModInput) -> dict[str, Any]:
    data = CreateModInput.model_validate(input)
    client = info.context["clients"]["mod_service"]
    resp = await client.create_mod(data.title, data.author_id, data.filename, data.description)
    return CreateModResult(mod_id=resp.mod_id, s3_key=resp.s3_key, upload_url=resp.upload_url).model_dump()


class SetStatusInput(BaseModel):
    mod_id: int
    status: ModStatus

    @field_validator("mod_id", mode="before")
    def validate_mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")


@mod_mutation.field("setStatus")
@handle_grpc_errors
async def resolve_set_status_mod(parent: object, info: GraphQLResolveInfo, input: SetStatusInput) -> bool:
    data = SetStatusInput.model_validate(input)
    client = info.context["clients"]["mod_service"]
    resp = await client.set_status_mod(data.mod_id, data.status.value)
    return resp.success  # type: ignore
