from ariadne import MutationType
from gateway.clients.comment import create_comment_rpc
from gateway.clients.comment import edit_comment_rpc
from gateway.clients.comment import delete_comment_rpc
from gateway.clients.rating import rate_mod_rpc
mutation = MutationType()

@mutation.field("createComment")
def resolve_create_comment(_, info, input):
    resp = create_comment_rpc(input["mod_id"], input["author_id"], input["text"])
    return str(resp.comment_id)

@mutation.field("editComment")
def resolve_edit_comment(_, info, input):
    resp = edit_comment_rpc(input["comment_id"], input["text"])
    return bool(resp.success)

@mutation.field("deleteComment")
def resolve_delete_comment(_, info, input):
    resp = delete_comment_rpc(input["comment_id"])
    return bool(resp.success)

@mutation.field("addrate")
def resolve_add_rate(_, info, input):
    resp = rate_mod_rpc(input["mod_id"], input["author_id"], input["rate"])
    return str(resp.rate_id)