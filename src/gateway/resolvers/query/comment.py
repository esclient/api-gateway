from ariadne import ObjectType
from pydantic import BaseModel, field_validator

from gateway.clients.comment import get_comments_rpc
from gateway.helpers.id_helper import validate_and_convert_id


class GetCommentsInput(BaseModel):
    mod_id: int

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v):
        return validate_and_convert_id(v, "mod_id")


class GetCommentsResult(BaseModel):
    id: int
    text: str
    author_id: int
    created_at: int
    edited_at: int | None = None

    @field_validator("edited_at", mode="before")
    def _edited_at(cls, v):
        return None if v == 0 else v


comment_query = ObjectType("CommentQuery")


@comment_query.field("getComments")
def resolve_get_comments(_, info, input: GetCommentsInput):
    data = GetCommentsInput.model_validate(input)
    resp = get_comments_rpc(data.mod_id)
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
