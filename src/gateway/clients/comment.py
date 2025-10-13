

from gateway.stubs import comment_pb2, comment_pb2_grpc

from .base_client import GrpcClient


class CommentServiceClient(GrpcClient):
    def _initialize_stub(self) -> None:
        self._stub = comment_pb2_grpc.CommentServiceStub(self._channel)  # type: ignore

    async def create_comment(self, mod_id: int, author_id: int, text: str) -> comment_pb2.CreateCommentResponse:
        request = comment_pb2.CreateCommentRequest(mod_id=mod_id, author_id=author_id, text=text)
        return await self.call(self._stub.CreateComment, request)

    async def edit_comment(self, comment_id: int, text: str) -> comment_pb2.EditCommentResponse:
        request = comment_pb2.EditCommentRequest(comment_id=comment_id, text=text)
        return await self.call(self._stub.EditComment, request)

    async def delete_comment(self, comment_id: int) -> comment_pb2.DeleteCommentResponse:
        request = comment_pb2.DeleteCommentRequest(comment_id=comment_id)
        return await self.call(self._stub.DeleteComment, request)

    async def get_comments(self, mod_id: int) -> comment_pb2.GetCommentsResponse:
        request = comment_pb2.GetCommentsRequest(mod_id=mod_id)
        return await self.call(self._stub.GetComments, request)
