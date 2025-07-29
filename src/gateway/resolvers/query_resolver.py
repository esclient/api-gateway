from ariadne import QueryType
from gateway.clients.comment import get_comments_rpc
query = QueryType()


@query.field("getComments")
def resolve_get_comments(_, info, input):
    resp = get_comments_rpc(int(input["mod_id"]))
    print(resp)
    return [
        {
            "id": item.id,
            "text": item.text,
            "author_id": item.author_id,
            "created_at": item.created_at

        }
        for item in resp.comments
    ]