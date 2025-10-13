import asyncio
import logging

import uvicorn
from ariadne import load_schema_from_path, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.explorer import ExplorerGraphiQL

from gateway.clients.client_factory import GRPCClientFactory
from gateway.resolvers.mutation.comment import comment_mutation
from gateway.resolvers.mutation.mod import mod_mutation
from gateway.resolvers.mutation.root import mutation
from gateway.resolvers.query.comment import comment_query
from gateway.resolvers.query.mod import mod_query
from gateway.resolvers.query.root import query
from gateway.settings import Settings

from .esclient_graphql import GQLContextViewer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
clients_factory = GRPCClientFactory(settings)

app = GraphQL(schema, debug=True, explorer=ExplorerGraphiQL(), context_value=context_viewer.get_current)


async def main():  # type: ignore
    logger.info("Инициализация gRPC клиентов...")
    comment_client = clients_factory.get_comment_client()
    mod_client = clients_factory.get_mod_client()
    rating_client = clients_factory.get_rating_client()
    logger.info("gRPC клиенты инициализированы.")

    context_viewer.clients = {
        "comment_service": comment_client,
        "mod_service": mod_client,
        "rating_service": rating_client,
    }

    app = GraphQL(
        schema,
        debug=True,
        explorer=ExplorerGraphiQL(),
        context_value=context_viewer.get_current,
    )

    config = uvicorn.Config(app=app, host=settings.host, port=settings.port, reload=True)
    server = uvicorn.Server(config)

    try:
        await server.serve()
    finally:
        logger.info("Закрытие gRPC каналов...")
        await clients_factory.close_all()
        logger.info("Все соединения закрыты.")


if __name__ == "__main__":
    asyncio.run(main())  # type: ignore
