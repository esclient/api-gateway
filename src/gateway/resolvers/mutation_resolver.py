from ariadne import MutationType
from gateway.clients.comment import create_comment_rpc
from gateway.clients.comment import edit_comment_rpc
from gateway.clients.comment import delete_comment_rpc
from gateway.clients.rating import rate_mod_rpc
from gateway.clients.mod import create_mod_rpc
from gateway.clients.mod import set_status_mod_rpc
from ..helpers.id_helper import validate_and_convert_id


mutation = MutationType()

@mutation.field("createComment")
def resolve_create_comment(_, info, input):
    mod_id = validate_and_convert_id(input["mod_id"], "mod_id")
    author_id = validate_and_convert_id(input["author_id"], "author_id")
    resp = create_comment_rpc(mod_id, author_id, input["text"])
    return str(resp.comment_id)

@mutation.field("editComment")
def resolve_edit_comment(_, info, input):
    comment_id = validate_and_convert_id(input["comment_id"], "comment_id")
    resp = edit_comment_rpc(comment_id, input["text"])
    return bool(resp.success)

@mutation.field("deleteComment")
def resolve_delete_comment(_, info, input):
    comment_id = validate_and_convert_id(input["comment_id"], "comment_id")
    resp = delete_comment_rpc(comment_id)
    return bool(resp.success)

@mutation.field("addRate")
def resolve_add_rate(_, info, input):
    mod_id = validate_and_convert_id(input["mod_id"], "mod_id")
    author_id = validate_and_convert_id(input["author_id"], "author_id")
    resp = rate_mod_rpc(mod_id, author_id, input["rate"])
    return str(resp.rate_id)

@mutation.field("createMod")
def resolve_create_mod(_, info, input):
    author_id = validate_and_convert_id(input["author_id"], "author_id")
    resp = create_mod_rpc(
        input["mod_title"],
        author_id,
        input["filename"],
        input["description"]
    )

    return {
        "mod_id": str(resp.mod_id),
        "s3_key": resp.s3_key,
        "upload_url": resp.upload_url
    }

@mutation.field("setStatus")
def resolve_set_status_mod(_, info, input):
    mod_id = validate_and_convert_id(input["mod_id"], "mod_id")
    resp = set_status_mod_rpc(
        mod_id,
        input["status"]
    )

    return resp.success