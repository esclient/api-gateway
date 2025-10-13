import grpc

from gateway.clients.comment import CommentServiceClient
from gateway.clients.mod import ModServiceClient
from gateway.clients.rating import RatingServiceClient


class GrpcClientFactory:
    def __init__(self, comment_service_url: str, mod_service_url: str, rating_service_url: str) -> None:
        self._comment_service_url = comment_service_url
        self._mod_service_url = mod_service_url
        self._rating_service_url = rating_service_url
        self._channels: dict[str, grpc.aio.Channel] = {}  # На всякий случай

    def _add_to_channels(self, url: str) -> None:
        if url not in self._channels:
            self._channels[url] = grpc.aio.insecure_channel(url)

    def get_comment_client(self) -> CommentServiceClient:
        url = self._comment_service_url
        self._add_to_channels(url)

        return CommentServiceClient(self._channels[url])

    def get_mod_client(self) -> ModServiceClient:
        url = self._mod_service_url
        self._add_to_channels(url)

        return ModServiceClient(self._channels[url])

    def get_rating_client(self) -> RatingServiceClient:
        url = self._rating_service_url
        self._add_to_channels(url)

        return RatingServiceClient(self._channels[url])

    async def close_all(self) -> None:
        for channel in self._channels.values():
            await channel.close()

    async def __aenter__(self):  # type: ignore
        return self

    async def __aexit__(self, exc_type, exc, tb):  # type: ignore
        await self.close_all()
