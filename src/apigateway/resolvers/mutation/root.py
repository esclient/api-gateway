from typing import Any

from ariadne import MutationType
from graphql import GraphQLResolveInfo

from ..grpc_error_wrapper import handle_grpc_errors

mutation = MutationType()


@mutation.field("comment")
@handle_grpc_errors
def resolve_comment_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}


@mutation.field("mod")
@handle_grpc_errors
def resolve_mod_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}


@mutation.field("rating")
@handle_grpc_errors
def resolve_rating_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}
