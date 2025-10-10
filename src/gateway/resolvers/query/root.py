from typing import Any

from ariadne import QueryType
from graphql import GraphQLResolveInfo

from ..grpc_error_wrapper import handle_grpc_errors

query = QueryType()


@query.field("comment")
@handle_grpc_errors
def resolve_comment_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}


@query.field("mod")
@handle_grpc_errors
def resolve_mod_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}
