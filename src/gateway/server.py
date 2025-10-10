import uvicorn
from ariadne.asgi import GraphQL
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.explorer import ExplorerGraphiQL

from .esclient_graphql import ESClientGQL, GQLContextViewer
from gateway.resolvers.mutation.comment import comment_mutation
from gateway.resolvers.mutation.mod import mod_mutation
from gateway.resolvers.mutation.root import mutation
from gateway.resolvers.query.comment import comment_query
from gateway.resolvers.query.mod import mod_query
from gateway.resolvers.query.root import query
from gateway.clients.client_factory import GRPCClientFactory, AsyncGRPCClientFactory
from gateway.settings import Settings

settings = Settings()

type_defs = load_schema_from_path("src/gateway/schema")

schema = make_executable_schema(
    type_defs,
    query,
    comment_query,
    mod_query,
    mutation,
    comment_mutation,
    mod_mutation,
)

context_viewer = GQLContextViewer()

app = GraphQL(
    schema,
    debug=True,
    explorer=ExplorerGraphiQL(),
    context_value=context_viewer.get_current
)

sync_clients_factory = GRPCClientFactory(settings)
async_clients_factory = AsyncGRPCClientFactory(settings)

#<Потом это можно будет заменить балансировщиком>#
#<Я ваще не понимаю, что я делаю 🙏🙏🙏>#
context_viewer.clients = {
    "comment_service": sync_clients_factory.get_comment_client(),
    "mod_service": sync_clients_factory.get_mod_client(),
    "rating_service": sync_clients_factory.get_rating_client()
}

if __name__ == "__main__":
    uvicorn.run(
        "gateway.server:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
