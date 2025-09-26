from enum import Enum
from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from gateway.clients.rating import rate_mod_rpc
from gateway.helpers.id_helper import validate_and_convert_id

rating_mutation = ObjectType("RatingMutation")


class RateType(str, Enum):
    RATE_UNSPECIFIED = "RATE_UNSPECIFIED"
    RATE_1 = "RATE_1"
    RATE_2 = "RATE_2"
    RATE_3 = "RATE_3"
    RATE_4 = "RATE_4"
    RATE_5 = "RATE_5"


class AddRateInput(BaseModel):
    mod_id: int
    author_id: int
    rate: RateType

    @field_validator("mod_id", mode="before")
    def validate_mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")

    @field_validator("author_id", mode="before")
    def validate_author_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "author_id")


@rating_mutation.field("addRate")
def resolve_add_rate(parent: object, info: GraphQLResolveInfo, input: AddRateInput) -> str:
    data = AddRateInput.model_validate(input)
    resp = rate_mod_rpc(data.mod_id, data.author_id, data.rate.value)
    return str(resp.rate_id)
