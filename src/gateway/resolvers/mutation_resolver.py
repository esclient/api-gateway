from ariadne import MutationType
from gateway.clients.comment import create_comment_rpc
from gateway.clients.comment import edit_comment_rpc
from gateway.clients.comment import delete_comment_rpc
from gateway.clients.rating import rate_mod_rpc
from gateway.clients.mod import create_mod_rpc
from gateway.clients.mod import set_status_mod_rpc
from gateway.helpers.id_helper import validate_and_convert_id
from pydantic import BaseModel, field_validator, ConfigDict

mutation = MutationType()

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

@mutation.field("createComment")
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

@mutation.field("editComment")
def resolve_edit_comment(_, info, input: EditCommentInput) -> bool:
    data = EditCommentInput.model_validate(input)
    resp = edit_comment_rpc(data.comment_id, data.text)
    return resp.success

class DeleteCommentInput(BaseModel):
    comment_id: int

    @field_validator("comment_id", mode="before")
    def _comment_id(cls, v):
        return validate_and_convert_id(v, "comment_id")

@mutation.field("deleteComment")
def resolve_delete_comment(_, info, input: DeleteCommentInput) -> bool:
    data = DeleteCommentInput.model_validate(input)
    resp = delete_comment_rpc(data.comment_id)
    return resp.success

class AddRateInput(BaseModel):
    mod_id: int
    author_id: int
    rate: enumerate

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v):
        return validate_and_convert_id(v, "mod_id")

    @field_validator("author_id", mode="before")
    def _author_id(cls, v):
        return validate_and_convert_id(v, "author_id")

@mutation.field("addRate")
def resolve_add_rate(_, info, input: AddRateInput) -> str:
    data = AddRateInput.model_validate(input)
    resp = rate_mod_rpc(data.mod_id, data.author_id, data.rate)
    return str(resp.rate_id)

class CreateModInput(BaseModel):
    mod_title: str
    author_id: int
    filename: str
    description: str

    @field_validator("author_id", mode="before")
    def _author_id(cls, v):
        return validate_and_convert_id(v, "author_id")

class CreateModResult(BaseModel):
    mod_id: int
    s3_key: str
    upload_url: str

@mutation.field("createMod")
def resolve_create_mod(_, info, input: CreateModInput):
    data = CreateModInput.model_validate(input)
    resp = create_mod_rpc(
        data.mod_title,
        data.author_id,
        data.filename,
        data.description
    )

    return CreateModResult(
        mod_id=resp.mod_id,
        s3_key=resp.s3_key,
        upload_url=resp.upload_url
    ).model_dump()

class SetStatusInput(BaseModel):
    mod_id: int
    status: enumerate

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v):
        return validate_and_convert_id(v, "mod_id")

@mutation.field("setStatus")
def resolve_set_status_mod(_, info, input):
    data = SetStatusInput.model_validate(input)
    resp = set_status_mod_rpc(
        data.mod_id,
        data.status
    )

    return resp.success