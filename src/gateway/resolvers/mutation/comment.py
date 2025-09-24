from ariadne import MutationType
from gateway.clients.comment import create_comment_rpc
from gateway.clients.comment import edit_comment_rpc
from gateway.clients.comment import delete_comment_rpc
from gateway.helpers.id_helper import validate_and_convert_id
from pydantic import BaseModel, field_validator, ConfigDict


comment_mutation = MutationType()

class CreateCommentInput(BaseModel):
    mod_id: int
    author_id: int
    text: str

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v):
        return validate_and_convert_id(v, "mod_id")

    @field_validator("author_id", mode="before")
    def _author_id(cls, v):
        return validate_and_convert_id(v, "author_id")

@comment_mutation.field("createComment")
def resolve_create_comment(_, info, input: CreateCommentInput) -> str:
    data = CreateCommentInput.model_validate(input)
    resp = create_comment_rpc(data.mod_id, data.author_id, data.text)
    return str(resp.comment_id)

class EditCommentInput(BaseModel):
    comment_id: int
    text: str

    @field_validator("comment_id", mode="before")
    def _comment_id(cls, v):
        return validate_and_convert_id(v, "comment_id")

@comment_mutation.field("editComment")
def resolve_edit_comment(_, info, input: EditCommentInput) -> bool:
    data = EditCommentInput.model_validate(input)
    resp = edit_comment_rpc(data.comment_id, data.text)
    return resp.success

class DeleteCommentInput(BaseModel):
    comment_id: int

    @field_validator("comment_id", mode="before")
    def _comment_id(cls, v):
        return validate_and_convert_id(v, "comment_id")

@comment_mutation.field("deleteComment")
def resolve_delete_comment(_, info, input: DeleteCommentInput) -> bool:
    data = DeleteCommentInput.model_validate(input)
    resp = delete_comment_rpc(data.comment_id)
    return resp.success