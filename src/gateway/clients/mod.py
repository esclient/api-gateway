

from gateway.stubs import mod_pb2, mod_pb2_grpc

from .base_client import GrpcClient


class ModServiceClient(GrpcClient):
    def _initialize_stub(self) -> None:
        self._stub = mod_pb2_grpc.ModServiceStub(self._channel)  # type: ignore

    async def create_mod(
        self, title: str, author_id: int, filename: str, description: str
    ) -> mod_pb2.CreateModResponse:
        request = mod_pb2.CreateModRequest(title=title, author_id=author_id, filename=filename, description=description)
        return await self.call(self._stub.CreateMod, request)

    async def set_status_mod(self, mod_id: int, status: str) -> mod_pb2.SetStatusResponse:
        request = mod_pb2.SetStatusRequest(mod_id=mod_id, status=status)
        return await self.call(self._stub.SetStatus, request)

    async def get_mod_download_link(self, mod_id: int) -> mod_pb2.GetModDownloadLinkResponse:
        request = mod_pb2.GetModDownloadLinkRequest(mod_id=mod_id)
        return await self.call(self._stub.GetModDownloadLink, request)

    async def get_mods(self) -> mod_pb2.GetModsResponse:
        request = mod_pb2.GetModsRequest()
        return await self.call(self._stub.GetMods, request)
