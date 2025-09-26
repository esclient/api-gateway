from typing import Any

from ariadne import MutationType
from graphql import GraphQLResolveInfo

mutation = MutationType()


@mutation.field("comment")
def resolve_comment_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}


@mutation.field("mod")
def resolve_mod_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}


@mutation.field("rating")
def resolve_rating_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}
