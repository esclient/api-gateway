import uvicorn
from ariadne import make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from ariadne.asgi import GraphQL

from gateway.resolvers.mutation.root import mutation
from gateway.resolvers.mutation.comment import comment_mutation
from gateway.resolvers.mutation.mod import mod_mutation
from gateway.resolvers.query.root import query
from gateway.resolvers.query.comment import comment_query
from gateway.resolvers.query.mod import mod_query
from gateway.settings import Settings

settings = Settings()

schema = make_executable_schema(
    load_schema_from_path("src/gateway/schema"),
    query,
    comment_query,
    mod_query,
    mutation,
    comment_mutation,
    mod_mutation
)

app = GraphQL(
    schema,
    debug=True,
    explorer=ExplorerGraphiQL(),
)

if __name__ == "__main__":
    uvicorn.run(
        "gateway.server:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
