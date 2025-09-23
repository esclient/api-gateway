from ariadne import ObjectType
from gateway.clients.comment import get_comments_rpc

comment_query = ObjectType("CommentQuery")

@comment_query.field("getComments")
def resolve_get_comments(_, info, input):
    resp = get_comments_rpc(int(input["mod_id"]))
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
