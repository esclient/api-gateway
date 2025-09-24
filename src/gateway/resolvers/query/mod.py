from ariadne import ObjectType
from gateway.clients.mod import get_mod_download_link_rpc
from gateway.helpers.id_helper import validate_and_convert_id
from pydantic import BaseModel, field_validator

class GetModDownloadLinkInput(BaseModel):
    mod_id: int

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v):
        return validate_and_convert_id(v, "mod_id")

mod_query = ObjectType("Query")

@mod_query.field("getModDownloadLink")
def resolve_get_mod_download_link(_, info, input) -> str:
    data = GetModDownloadLinkInput.model_validate(input)
    resp = get_mod_download_link_rpc(data.mod_id)
    return resp.link_url
