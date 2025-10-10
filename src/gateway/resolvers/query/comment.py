from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from gateway.helpers.id_helper import validate_and_convert_id


class GetCommentsInput(BaseModel):
    mod_id: int

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")


class GetCommentsResult(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: int
    edited_at: int | None = None

    @field_validator("edited_at", mode="before")
    def _edited_at(cls, v: Any) -> Any | None:
        return None if v == 0 else v


comment_query = ObjectType("CommentQuery")


@comment_query.field("getComments")
def resolve_get_comments(parent: object, info: GraphQLResolveInfo, input: GetCommentsInput) -> list[dict[str, Any]]:
    data = GetCommentsInput.model_validate(input)
    client = info.context["clients"]["comment_service"]
    resp = client.get_comments(data.mod_id)
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
