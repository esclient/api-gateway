import grpc

import gateway.stubs.rating_pb2
import gateway.stubs.rating_pb2_grpc

_channel = grpc.insecure_channel("host.docker.internal:7777")
_stub = gateway.stubs.rating_pb2_grpc.RatingServiceStub(_channel)  # type: ignore


def rate_mod_rpc(mod_id: int, author_id: int, rate: str) -> gateway.stubs.rating_pb2.RateModResponse:
    req = gateway.stubs.rating_pb2.RateModRequest(mod_id=mod_id, author_id=author_id, rate=rate)
    return _stub.RateMod(req)  # type: ignore


def get_rates_rpc(mod_id: int) -> gateway.stubs.rating_pb2.GetRatesResponse:
    req = gateway.stubs.rating_pb2.GetRatesRequest(mod_id=mod_id)
    return _stub.GetRates(req)  # type: ignore
