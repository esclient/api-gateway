from gateway.stubs import rating_pb2, rating_pb2_grpc
from google.protobuf import message as _message
from typing import Dict, Any
from .base_client import GRPCClient, AsyncGRPCClient

class RatingServiceClient(GRPCClient):
    _RPC_REQUEST_CLASSES = {
        "RateMod": rating_pb2.RateModRequest,
        "GetRates": rating_pb2.GetRatesRequest,
    }

    def _initialize_stub(self):
        self._stub = rating_pb2_grpc.RatingServiceStub(self._channel)

    def _create_request(self, rpc_name: str, request_data: Dict[str, Any]) -> _message.Message:
        request_class = RatingServiceClient._RPC_REQUEST_CLASSES.get(rpc_name)
        if not request_class:
            raise ValueError(f"Неизветсный RPC метод: {rpc_name}")
        
        return request_class(**request_data)
    
    # *** #

    def rate_mod(self, mod_id: int, author_id: int, rate: str) -> rating_pb2.RateModResponse:
        return self.call_rpc("RateMod", {
            "mod_id": mod_id,
            "author_id": author_id,
            "rate": rate
        })


    def get_rates(self, mod_id: int) -> rating_pb2.GetRatesResponse:
        return self.call_rpc("GetRates", { "mod_id": mod_id })

class AsyncRatingServiceClient(AsyncGRPCClient):
    _RPC_REQUEST_CLASSES = {
        "RateMod": rating_pb2.RateModRequest,
        "GetRates": rating_pb2.GetRatesRequest,
    }

    def _initialize_stub(self):
        self._stub = rating_pb2_grpc.RatingServiceStub(self._channel)
    
    def _create_request(self, rpc_name: str, request_data: Dict[str, Any]) -> _message.Message:
        request_class = RatingServiceClient._RPC_REQUEST_CLASSES.get(rpc_name)
        if not request_class:
            raise ValueError(f"Неизветсный RPC метод: {rpc_name}")
        
        return request_class(**request_data)
    
    # *** #

    async def rate_mod(self, mod_id: int, author_id: int, rate: str) -> rating_pb2.RateModResponse:
        return self.call_rpc("RateMod", {
            "mod_id": mod_id,
            "author_id": author_id,
            "rate": rate
        })


    async def get_rates(self, mod_id: int) -> rating_pb2.GetRatesResponse:
        return self.call_rpc("GetRates", { "mod_id": mod_id })
