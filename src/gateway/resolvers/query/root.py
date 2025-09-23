from ariadne import QueryType

query = QueryType()

@query.field("comment")
def resolve_comment_root(*_):
    return {}

@query.field("mod")
def resolve_mod_root(*_):
    return {}
