from apigateway.clients.base_client import GrpcClient
from apigateway.stubs.comment import comment_pb2, comment_pb2_grpc


class CommentServiceClient(GrpcClient[comment_pb2_grpc.CommentServiceStub]):
    def _initialize_stub(self) -> comment_pb2_grpc.CommentServiceStub:
        return comment_pb2_grpc.CommentServiceStub(self._channel)  # type: ignore[no-untyped-call]

    async def create_comment(self, mod_id: int, author_id: int, text: str) -> comment_pb2.CreateCommentResponse:
        request = comment_pb2.CreateCommentRequest(mod_id=mod_id, author_id=author_id, text=text)
        return await self.call(self._stub.CreateComment, request)

    async def edit_comment(self, comment_id: int, text: str) -> comment_pb2.EditCommentResponse:
        request = comment_pb2.EditCommentRequest(comment_id=comment_id, text=text)
        return await self.call(self._stub.EditComment, request)

    async def set_status_comment(self, comment_id: int, status: str) -> comment_pb2.SetStatusResponse:
        request = comment_pb2.SetStatusRequest(comment_id=comment_id, status=status)
        return await self.call(self._stub.SetStatus, request)

    async def get_comments(self, mod_id: int) -> comment_pb2.GetCommentsResponse:
        request = comment_pb2.GetCommentsRequest(mod_id=mod_id)
        return await self.call(self._stub.GetComments, request)
