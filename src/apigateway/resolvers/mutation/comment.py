from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from apigateway.helpers.id_helper import validate_and_convert_id

from ..grpc_error_wrapper import handle_grpc_errors

comment_mutation = ObjectType("CommentMutation")


class CreateCommentInput(BaseModel):
    mod_id: int
    author_id: int
    text: str

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")

    @field_validator("author_id", mode="before")
    def _author_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "author_id")


@comment_mutation.field("createComment")
@handle_grpc_errors
async def resolve_create_comment(parent: object, info: GraphQLResolveInfo, input: CreateCommentInput) -> str:
    data = CreateCommentInput.model_validate(input)
    client = info.context["clients"]["comment_service"]
    resp = await client.create_comment(data.mod_id, data.author_id, data.text)
    return str(resp.comment_id)


class EditCommentInput(BaseModel):
    comment_id: int
    text: str

    @field_validator("comment_id", mode="before")
    def _comment_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "comment_id")


@comment_mutation.field("editComment")
@handle_grpc_errors
async def resolve_edit_comment(parent: object, info: GraphQLResolveInfo, input: EditCommentInput) -> bool:
    data = EditCommentInput.model_validate(input)
    client = info.context["clients"]["comment_service"]
    resp = await client.edit_comment(data.comment_id, data.text)
    return resp.success  # type: ignore


class DeleteCommentInput(BaseModel):
    comment_id: int

    @field_validator("comment_id", mode="before")
    def _comment_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "comment_id")


@comment_mutation.field("deleteComment")
@handle_grpc_errors
async def resolve_delete_comment(parent: object, info: GraphQLResolveInfo, input: DeleteCommentInput) -> bool:
    data = DeleteCommentInput.model_validate(input)
    client = info.context["clients"]["comment_service"]
    resp = await client.delete_comment(data.comment_id)
    return resp.success  # type: ignore
