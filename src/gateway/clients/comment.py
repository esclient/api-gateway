from collections.abc import Coroutine
from typing import Any, ClassVar

from google.protobuf import message as _message

from gateway.stubs import comment_pb2, comment_pb2_grpc

from .base_client import AsyncGRPCClient, GRPCClient


class CommentServiceClient(GRPCClient):
    _RPC_REQUEST_CLASSES: ClassVar[dict[str, type[_message.Message]]] = {
        "CreateComment": comment_pb2.CreateCommentRequest,
        "EditComment": comment_pb2.EditCommentRequest,
        "DeleteComment": comment_pb2.DeleteCommentRequest,
        "GetComments": comment_pb2.GetCommentsRequest,
    }

    def _initialize_stub(self) -> None:
        self._stub = comment_pb2_grpc.CommentServiceStub(self._channel)  # type: ignore

    def _create_request(self, rpc_name: str, request_data: dict[str, Any]) -> _message.Message:
        request_class = CommentServiceClient._RPC_REQUEST_CLASSES.get(rpc_name)
        if not request_class:
            raise ValueError(f"Неизветсный RPC метод: {rpc_name}")

        return request_class(**request_data)

    # Вообще я написал универсальный "call_rpc". Но обёртки никто не отменял :)
    # Как минимум благодаря обёртке мы можем проставить типизацию

    def create_comment(self, mod_id: int, author_id: int, text: str) -> comment_pb2.CreateCommentResponse:
        return self.call_rpc("CreateComment", {"mod_id": mod_id, "author_id": author_id, "text": text})  # type: ignore[return-value]

    def edit_comment(self, comment_id: int, text: str) -> comment_pb2.EditCommentResponse:
        return self.call_rpc("EditComment", {"comment_id": comment_id, "text": text})  # type: ignore[return-value]

    def delete_comment(self, comment_id: int) -> comment_pb2.DeleteCommentResponse:
        return self.call_rpc("DeleteComment", {"comment_id": comment_id})  # type: ignore[return-value]

    def get_comments(self, mod_id: int) -> comment_pb2.GetCommentsResponse:
        return self.call_rpc("GetComments", {"mod_id": mod_id})  # type: ignore[return-value]


class AsyncCommentServiceClient(AsyncGRPCClient):
    _RPC_REQUEST_CLASSES: ClassVar[dict[str, type[_message.Message]]] = {
        "CreateComment": comment_pb2.CreateCommentRequest,
        "EditComment": comment_pb2.EditCommentRequest,
        "DeleteComment": comment_pb2.DeleteCommentRequest,
        "GetComments": comment_pb2.GetCommentsRequest,
    }

    def _initialize_stub(self) -> None:
        self._stub = comment_pb2_grpc.CommentServiceStub(self._channel)  # type: ignore

    def _create_request(self, rpc_name: str, request_data: dict[str, Any]) -> _message.Message:
        request_class = CommentServiceClient._RPC_REQUEST_CLASSES.get(rpc_name)
        if not request_class:
            raise ValueError(f"Неизветсный RPC метод: {rpc_name}")

        return request_class(**request_data)

    # *** #

    async def create_comment(
        self, mod_id: int, author_id: int, text: str
    ) -> Coroutine[Any, Any, comment_pb2.CreateCommentResponse]:
        return self.call_rpc("CreateComment", {"mod_id": mod_id, "author_id": author_id, "text": text})  # type: ignore[return-value]

    async def edit_comment(self, comment_id: int, text: str) -> Coroutine[Any, Any, comment_pb2.EditCommentResponse]:
        return self.call_rpc("EditComment", {"comment_id": comment_id, "text": text})  # type: ignore[return-value]

    async def delete_comment(self, comment_id: int) -> Coroutine[Any, Any, comment_pb2.DeleteCommentResponse]:
        return self.call_rpc("DeleteComment", {"comment_id": comment_id})  # type: ignore[return-value]

    async def get_comments(self, mod_id: int) -> Coroutine[Any, Any, comment_pb2.GetCommentsResponse]:
        return self.call_rpc("GetComments", {"mod_id": mod_id})  # type: ignore[return-value]
