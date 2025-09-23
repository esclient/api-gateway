from ariadne import ObjectType
from gateway.clients.mod import get_mod_download_link_rpc

mod_query = ObjectType("ModQuery")

@mod_query.field("getModDownloadLink")
def resolve_get_mod_download_link(_, info, input):
    resp = get_mod_download_link_rpc(int(input["mod_id"]))
    return resp.link_url
