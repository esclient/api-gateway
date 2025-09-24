from ariadne import ObjectType
from gateway.clients.rating import rate_mod_rpc
from gateway.clients.mod import create_mod_rpc
from gateway.clients.mod import set_status_mod_rpc
from gateway.helpers.id_helper import validate_and_convert_id
from pydantic import BaseModel, field_validator, ConfigDict
from enum import Enum

mod_mutation = ObjectType("ModMutation")

class RateType(str, Enum):
    """Define the possible rating values to match GraphQL Rate enum"""
    RATE_UNSPECIFIED = "RATE_UNSPECIFIED"
    RATE_1 = "RATE_1"
    RATE_2 = "RATE_2"
    RATE_3 = "RATE_3"
    RATE_4 = "RATE_4"
    RATE_5 = "RATE_5"

class ModStatus(str, Enum):
    """Define the possible mod status values to match GraphQL ModStatus enum"""
    MOD_STATUS_UNSPECIFIED = "MOD_STATUS_UNSPECIFIED"
    MOD_STATUS_UPLOADED = "MOD_STATUS_UPLOADED"
    MOD_STATUS_BANNED = "MOD_STATUS_BANNED"
    MOD_STATUS_HIDDEN = "MOD_STATUS_HIDDEN"


class AddRateInput(BaseModel):
    mod_id: int
    author_id: int
    rate: RateType  
    
    @field_validator("mod_id", mode="before")
    def validate_mod_id(cls, v):
        return validate_and_convert_id(v, "mod_id")
    
    @field_validator("author_id", mode="before")
    def validate_author_id(cls, v):
        return validate_and_convert_id(v, "author_id")

@mod_mutation.field("addRate")
def resolve_add_rate(_, info, input: AddRateInput) -> str:
    data = AddRateInput.model_validate(input)
    resp = rate_mod_rpc(data.mod_id, data.author_id, data.rate.value)  # Use .value to get the actual value
    return str(resp.rate_id)

class CreateModInput(BaseModel):
    mod_title: str
    author_id: int
    filename: str
    description: str
    
    @field_validator("author_id", mode="before")
    def validate_author_id(cls, v):
        return validate_and_convert_id(v, "author_id")

class CreateModResult(BaseModel):
    mod_id: int
    s3_key: str
    upload_url: str

@mod_mutation.field("createMod")
def resolve_create_mod(_, info, input: CreateModInput):
    data = CreateModInput.model_validate(input)
    resp = create_mod_rpc(
        data.mod_title,
        data.author_id,
        data.filename,
        data.description
    )
    return CreateModResult(
        mod_id=resp.mod_id,
        s3_key=resp.s3_key,
        upload_url=resp.upload_url
    ).model_dump()

class SetStatusInput(BaseModel):
    mod_id: int
    status: ModStatus  
    
    @field_validator("mod_id", mode="before")
    def validate_mod_id(cls, v):
        return validate_and_convert_id(v, "mod_id")

@mod_mutation.field("setStatus")
def resolve_set_status_mod(_, info, input):
    data = SetStatusInput.model_validate(input)
    resp = set_status_mod_rpc(
        data.mod_id,
        data.status.value  
    )
    return resp.success