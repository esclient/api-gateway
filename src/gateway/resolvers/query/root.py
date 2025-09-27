from typing import Any

from ariadne import QueryType
from graphql import GraphQLResolveInfo

query = QueryType()


@query.field("comment")
def resolve_comment_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}


@query.field("mod")
def resolve_mod_root(obj: Any, info: GraphQLResolveInfo, **kwargs: Any) -> dict[str, Any]:
    return {}
