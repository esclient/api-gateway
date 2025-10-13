

from gateway.stubs import rating_pb2, rating_pb2_grpc

from .base_client import GrpcClient


class RatingServiceClient(GrpcClient):
    def _initialize_stub(self) -> None:
        self._stub = rating_pb2_grpc.RatingServiceStub(self._channel)  # type: ignore

    async def rate_mod(self, mod_id: int, author_id: int, rate: str) -> rating_pb2.RateModResponse:
        request = rating_pb2.RateModRequest(mod_id=mod_id, author_id=author_id, rate=rate)
        return await self.call(self._stub.RateMod, request)

    async def get_rates(self, mod_id: int) -> rating_pb2.GetRatesResponse:
        request = rating_pb2.GetRatesRequest(mod_id=mod_id)
        return await self.call(self._stub.GetRates, request)
