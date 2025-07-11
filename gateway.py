import uvicorn
from ariadne import make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers
from ariadne.explorer import ExplorerGraphiQL
from ariadne.asgi import GraphQL

type_defs = load_schema_from_path("schema/schema.graphql")

from resolvers.mutation_resolver import mutation
from resolvers.query_resolver import query

schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    snake_case_fallback_resolvers,
)

app = GraphQL(
    schema,
    debug=True,
    explorer=ExplorerGraphiQL(),
)

if __name__ == "__main__":
    uvicorn.run(
        "gateway:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
