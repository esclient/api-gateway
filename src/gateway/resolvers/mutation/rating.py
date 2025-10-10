from enum import StrEnum
from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from gateway.helpers.id_helper import validate_and_convert_id

rating_mutation = ObjectType("RatingMutation")


class RateType(StrEnum):
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
    client = info.context["clients"]["rating_service"]
    resp = client.rate_mod(data.mod_id, data.author_id, data.rate.value)
    return str(resp.rate_id)
