import grpc
import gateway.stubs.mod_pb2_grpc, gateway.stubs.mod_pb2

_channel = grpc.insecure_channel("host.docker.internal:7777")
_stub = gateway.stubs.mod_pb2_grpc.ModServiceStub(_channel)

def create_mod_rpc(mod_title: str, author_id: int, filename: str, description: str) -> gateway.stubs.mod_pb2.CreateModResponse:
    req = gateway.stubs.mod_pb2.CreateModRequest(mod_title=mod_title, author_id=author_id, filename=filename, description=description)
    return _stub.CreateMod(req)

def confirm_upload_rpc(mod_id: int) -> gateway.stubs.mod_pb2.ConfirmUploadResponse:
    req = gateway.stubs.mod_pb2.ConfirmUploadRequest(mod_id=mod_id)
    return _stub.ConfirmUpload(req)