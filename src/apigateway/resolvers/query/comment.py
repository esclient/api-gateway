from datetime import datetime
from typing import Any

from ariadne import ObjectType
from google.protobuf.timestamp_pb2 import Timestamp
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from apigateway.helpers.datetime_helper import timestamp_to_datetime
from apigateway.helpers.id_helper import validate_and_convert_id
from apigateway.resolvers.grpc_error_wrapper import handle_grpc_errors

comment_query = ObjectType("CommentQuery")


class GetCommentsInput(BaseModel):
    mod_id: int

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")


class GetCommentsResult(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: datetime
    edited_at: datetime | None = None

    @field_validator("created_at", mode="before")
    def _created_at(cls, value: Timestamp) -> datetime:
        created_at = timestamp_to_datetime(value)
        if created_at is None:
            raise ValueError("created_at is missing")

        return created_at

    @field_validator("edited_at", mode="before")
    def _edited_at(cls, value: Timestamp) -> datetime | None:
        return timestamp_to_datetime(value)


@comment_query.field("getComments")
@handle_grpc_errors
async def resolve_get_comments(
    parent: object, info: GraphQLResolveInfo, input: GetCommentsInput
) -> list[dict[str, Any]]:
    data = GetCommentsInput.model_validate(input)
    client = info.context["clients"]["comment_service"]
    resp = await client.get_comments(data.mod_id)
    return [
        GetCommentsResult(
            id=item.id,
            text=item.text,
            author_id=item.author_id,
            created_at=item.created_at,
            edited_at=item.edited_at,
        ).model_dump()
        for item in resp.comments
    ]
