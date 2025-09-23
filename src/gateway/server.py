import uvicorn
from ariadne import make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from ariadne.asgi import GraphQL

from gateway.resolvers.mutation_resolver import mutation
from gateway.resolvers.query.root import query
from gateway.resolvers.query.comment import comment_query
from gateway.resolvers.query.mod import mod_query

type_defs = load_schema_from_path("src/gateway/schema")

schema = make_executable_schema(
    type_defs,
    query,
    comment_query,
    mod_query,
    mutation,
)

app = GraphQL(
    schema,
    debug=True,
    explorer=ExplorerGraphiQL(),
)

if __name__ == "__main__":
    uvicorn.run(
        "gateway.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
