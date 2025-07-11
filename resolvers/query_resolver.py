from ariadne import QueryType
query = QueryType()


@query.field("test")
def resolve_test(_, info):
    return True
