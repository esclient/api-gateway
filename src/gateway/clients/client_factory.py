import grpc

from gateway.clients.comment import CommentServiceClient
from gateway.clients.mod import ModServiceClient
from gateway.clients.rating import RatingServiceClient
from gateway.settings import Settings


class GRPCClientFactory:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._channels: dict[str, grpc.aio.Channel] = {}  # На всякий случай

    def _add_to_channels_if_needed(self, url: str) -> None:
        if url not in self._channels:
            self._channels[url] = grpc.aio.insecure_channel(url)

    def get_comment_client(self) -> CommentServiceClient:
        url = self._settings.comment_service_url
        self._add_to_channels_if_needed(url)

        return CommentServiceClient(self._channels[url])

    def get_mod_client(self) -> ModServiceClient:
        url = self._settings.mod_service_url
        self._add_to_channels_if_needed(url)

        return ModServiceClient(self._channels[url])

    def get_rating_client(self) -> RatingServiceClient:
        url = self._settings.rating_service_url
        self._add_to_channels_if_needed(url)

        return RatingServiceClient(self._channels[url])

    async def close_all(self) -> None:
        for channel in self._channels.values():
            await channel.close()

    async def __aenter__(self):  # type: ignore
        return self

    async def __aexit__(self, exc_type, exc, tb):  # type: ignore
        await self.close_all()
