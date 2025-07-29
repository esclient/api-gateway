from ariadne import QueryType
from gateway.clients.comment import get_comments_rpc
query = QueryType()


@query.field("getComments")
def resolve_get_comments(_, info, input):
    resp = get_comments_rpc(input["mod_id"])
    print(resp)
    return str(resp)