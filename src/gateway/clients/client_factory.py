import grpc
from gateway.settings import Settings
from gateway.clients.comment import CommentServiceClient, AsyncCommentServiceClient
from gateway.clients.mod import ModServiceClient, AsyncModServiceClient
from gateway.clients.rating import RatingServiceClient, AsyncRatingServiceClient


class GRPCClientFactory:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._channels = {}  # На всякий случай

    def _add_to_channels_if_needed(self, url):
        if url not in self._channels:
            self._channels[url] = grpc.insecure_channel(url)

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
    
    def close_all(self):
        for channel in self._channels.values():
            channel.close()

class AsyncGRPCClientFactory:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._channels = {}  # На всякий случай

    def _add_to_channels_if_needed(self, url):
        if url not in self._channels:
            self._channels[url] = grpc.aio.insecure_channel(url)

    async def get_comment_client(self) -> AsyncCommentServiceClient:
        url = self._settings.comment_service_url
        self._add_to_channels_if_needed(url)
        
        return AsyncCommentServiceClient(self._channels[url])
    
    async def get_mod_client(self) -> AsyncModServiceClient:
        url = self._settings.mod_service_url
        self._add_to_channels_if_needed(url)

        return AsyncModServiceClient(self._channels[url])

    async def get_rating_client(self) -> AsyncRatingServiceClient:
        url = self._settings.rating_service_url
        self._add_to_channels_if_needed(url)

        return AsyncRatingServiceClient(self._channels[url])
    
    async def close_all(self):
        for channel in self._channels.values():
            channel.close()
