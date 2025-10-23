from typing import Any

from ariadne import ObjectType
from graphql import GraphQLResolveInfo
from pydantic import BaseModel, field_validator

from apigateway.helpers.id_helper import validate_and_convert_id

from ..grpc_error_wrapper import handle_grpc_errors


class GetRatesInput(BaseModel):
    mod_id: int

    @field_validator("mod_id", mode="before")
    def _mod_id(cls, v: Any) -> int:
        return validate_and_convert_id(v, "mod_id")


rating_query = ObjectType("RatingQuery")


@rating_query.field("getRates")
@handle_grpc_errors
async def resolve_get_rates(parent: object, info: GraphQLResolveInfo, input: GetRatesInput) -> dict[str, int]:
    data = GetRatesInput.model_validate(input)
    client = info.context["clients"]["rating_service"]
    resp = await client.get_rates(data.mod_id)

    return {
        "rates_total": resp.rates_total,
        "rate_1": resp.rate_1,
        "rate_2": resp.rate_2,
        "rate_3": resp.rate_3,
        "rate_4": resp.rate_4,
        "rate_5": resp.rate_5,
    }
