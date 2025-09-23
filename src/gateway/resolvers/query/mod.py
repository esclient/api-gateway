from ariadne import ObjectType
from gateway.clients.mod import get_mod_download_link_rpc
from ...helpers.id_helper import validate_and_convert_id

mod_query = ObjectType("ModQuery")

@mod_query.field("getModDownloadLink")
def resolve_get_mod_download_link(_, info, input):
    mod_id = validate_and_convert_id(input["mod_id"], "mod_id")
    resp = get_mod_download_link_rpc(mod_id)
    return resp.link_url
