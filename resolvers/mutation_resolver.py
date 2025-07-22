from ariadne import MutationType
from clients.comment import create_comment_rpc
from clients.comment import delete_comment_rpc
mutation = MutationType()

@mutation.field("createComment")
def resolve_create_comment(_, info, input):
    resp = create_comment_rpc(input["mod_id"], input["author_id"], input["text"])
    return str(resp.comment_id)

@mutation.field("deleteComment")
def resolve_delete_comment(_, info, input):
    resp = delete_comment_rpc(input["comment_id"])
    return bool(resp.success)