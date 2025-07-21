import grpc
import stubs.comment_pb2_grpc, stubs.comment_pb2

_channel = grpc.insecure_channel("localhost:50051")
_stub = stubs.comment_pb2_grpc.CommentServiceStub(_channel)

def create_comment_rpc(mod_id: int, author_id: int, text: str) -> stubs.comment_pb2.CreateCommentResponse:
    req = stubs.comment_pb2.CreateCommentRequest(mod_id=mod_id, author_id=author_id, text=text)
    return _stub.CreateComment(req)


def edit_comment_rpc(
    comment_id: int, text: str
) -> stubs.comment_pb2.EditCommentResponse:
    req = stubs.comment_pb2.EditCommentRequest(
        comment_id_id=comment_id, text=text
    )
    return _stub.EditComment(req)
