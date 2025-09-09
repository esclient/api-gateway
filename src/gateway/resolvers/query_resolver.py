from ariadne import QueryType
from gateway.clients.comment import get_comments_rpc
from gateway.clients.mod import get_mod_download_link_rpc

query = QueryType()


@query.field("getComments")
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


@query.field("getModDownloadLink")
def resolve_get_mod_download_link(_, info, input):
    resp = get_mod_download_link_rpc(int(input["mod_id"]))
    return resp.link_url
