import grpc

import gateway.stubs.mod_pb2
import gateway.stubs.mod_pb2_grpc
from gateway.converters.mod_status_converter import graphql_to_proto_mod_status

_channel = grpc.insecure_channel("host.docker.internal:7777")
_stub = gateway.stubs.mod_pb2_grpc.ModServiceStub(_channel)  # type: ignore


def create_mod_rpc(
    mod_title: str, author_id: int, filename: str, description: str
) -> gateway.stubs.mod_pb2.CreateModResponse:
    req = gateway.stubs.mod_pb2.CreateModRequest(
        mod_title=mod_title,
        author_id=author_id,
        filename=filename,
        description=description,
    )
    return _stub.CreateMod(req)  # type: ignore


def set_status_mod_rpc(mod_id: int, status: str) -> gateway.stubs.mod_pb2.SetStatusResponse:
    req = gateway.stubs.mod_pb2.SetStatusRequest(mod_id=mod_id, status=graphql_to_proto_mod_status(status))  # type: ignore
    return _stub.SetStatus(req)  # type: ignore


def get_mod_download_link_rpc(
    mod_id: int,
) -> gateway.stubs.mod_pb2.GetModDownloadLinkResponse:
    req = gateway.stubs.mod_pb2.GetModDownloadLinkRequest(mod_id=mod_id)
    return _stub.GetModDownloadLink(req)  # type: ignore


def get_mods_rpc() -> gateway.stubs.mod_pb2.GetModsResponse:
    req = gateway.stubs.mod_pb2.GetModsRequest()
    return _stub.GetMods(req)  # type: ignore
