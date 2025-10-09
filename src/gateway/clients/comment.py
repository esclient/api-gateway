import grpc

import gateway.stubs.comment_pb2
import gateway.stubs.comment_pb2_grpc
from gateway.settings import Settings

_settings = Settings()
_channel = grpc.insecure_channel(_settings.comment_service_url)
_stub = gateway.stubs.comment_pb2_grpc.CommentServiceStub(_channel)  # type: ignore


def create_comment_rpc(mod_id: int, author_id: int, text: str) -> gateway.stubs.comment_pb2.CreateCommentResponse:
    req = gateway.stubs.comment_pb2.CreateCommentRequest(mod_id=mod_id, author_id=author_id, text=text)
    return _stub.CreateComment(req)  # type: ignore


def edit_comment_rpc(comment_id: int, text: str) -> gateway.stubs.comment_pb2.EditCommentResponse:
    req = gateway.stubs.comment_pb2.EditCommentRequest(comment_id=comment_id, text=text)
    return _stub.EditComment(req)  # type: ignore


def delete_comment_rpc(
    comment_id: int,
) -> gateway.stubs.comment_pb2.DeleteCommentResponse:
    req = gateway.stubs.comment_pb2.DeleteCommentRequest(comment_id=comment_id)
    return _stub.DeleteComment(req)  # type: ignore


def get_comments_rpc(
    mod_id: int,
) -> gateway.stubs.comment_pb2.GetCommentsResponse:
    req = gateway.stubs.comment_pb2.GetCommentsRequest(mod_id=mod_id)
    return _stub.GetComments(req)  # type: ignore
