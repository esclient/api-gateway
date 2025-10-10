from collections.abc import Coroutine
from typing import Any, ClassVar

from google.protobuf import message as _message

from gateway.stubs import mod_pb2, mod_pb2_grpc

from .base_client import AsyncGRPCClient, GRPCClient


class ModServiceClient(GRPCClient):
    _RPC_REQUEST_CLASSES: ClassVar[dict[str, type[_message.Message]]] = {
        "CreateMod": mod_pb2.CreateModRequest,
        "SetStatus": mod_pb2.SetStatusRequest,
        "GetModDownloadLink": mod_pb2.GetModDownloadLinkRequest,
        "GetMods": mod_pb2.GetModsRequest,
    }

    def _initialize_stub(self) -> None:
        self._stub = mod_pb2_grpc.ModServiceStub(self._channel)  # type: ignore

    def _create_request(self, rpc_name: str, request_data: dict[str, Any]) -> _message.Message:
        request_class = ModServiceClient._RPC_REQUEST_CLASSES.get(rpc_name)
        if not request_class:
            raise ValueError(f"Неизветсный RPC метод: {rpc_name}")

        return request_class(**request_data)

    # *** #

    def create_mod(self, title: str, author_id: int, filename: str, description: str) -> mod_pb2.CreateModResponse:
        return self.call_rpc(
            "CreateMod", {"title": title, "author_id": author_id, "filename": filename, "description": description}
        )  # type: ignore[return-value]

    def set_status_mod(self, mod_id: int, status: str) -> mod_pb2.SetStatusResponse:
        return self.call_rpc("SetStatus", {"mod_id": mod_id, "status": status})  # type: ignore[return-value]

    def get_mod_download_link(self, mod_id: int) -> mod_pb2.GetModDownloadLinkResponse:
        return self.call_rpc("GetModDownloadLink", {"mod_id": mod_id})  # type: ignore[return-value]

    def get_mods(self) -> mod_pb2.GetModsResponse:
        return self.call_rpc("GetMods", {})  # type: ignore[return-value]


class AsyncModServiceClient(AsyncGRPCClient):
    _RPC_REQUEST_CLASSES: ClassVar[dict[str, type[_message.Message]]] = {
        "CreateMod": mod_pb2.CreateModRequest,
        "SetStatus": mod_pb2.SetStatusRequest,
        "GetModDownloadLink": mod_pb2.GetModDownloadLinkRequest,
        "GetMods": mod_pb2.GetModsRequest,
    }

    def _initialize_stub(self) -> None:
        self._stub = mod_pb2_grpc.ModServiceStub(self._channel)  # type: ignore

    def _create_request(self, rpc_name: str, request_data: dict[str, Any]) -> _message.Message:
        request_class = ModServiceClient._RPC_REQUEST_CLASSES.get(rpc_name)
        if not request_class:
            raise ValueError(f"Неизветсный RPC метод: {rpc_name}")

        return request_class(**request_data)

    # *** #

    async def create_mod(
        self, title: str, author_id: int, filename: str, description: str
    ) -> Coroutine[Any, Any, mod_pb2.CreateModResponse]:
        return self.call_rpc(
            "CreateMod", {"title": title, "author_id": author_id, "filename": filename, "description": description}
        )  # type: ignore[return-value]

    async def set_status_mod(self, mod_id: int, status: str) -> Coroutine[Any, Any, mod_pb2.SetStatusResponse]:
        return self.call_rpc("SetStatus", {"mod_id": mod_id, "status": status})  # type: ignore[return-value]

    async def get_mod_download_link_rpc(self, mod_id: int) -> Coroutine[Any, Any, mod_pb2.GetModDownloadLinkResponse]:
        return self.call_rpc("GetModDownloadLink", {"mod_id": mod_id})  # type: ignore[return-value]

    async def get_mods(self) -> Coroutine[Any, Any, mod_pb2.GetModsResponse]:
        return self.call_rpc("GetMods", {})  # type: ignore[return-value]
