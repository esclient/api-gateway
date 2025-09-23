from ariadne import ObjectType
from gateway.clients.comment import get_comments_rpc
from ...helpers.id_helper import validate_and_convert_id

comment_query = ObjectType("CommentQuery")

@comment_query.field("getComments")
def resolve_get_comments(_, info, input):
    mod_id = validate_and_convert_id(input["mod_id"], "mod_id")
    resp = get_comments_rpc(mod_id)
    return [
        {
            "id": item.id,
            "text": item.text,
            "author_id": item.author_id,
            "created_at": item.created_at,
            "edited_at": item.edited_at if item.edited_at != 0 else None,
        }
        for item in resp.comments
    ]
