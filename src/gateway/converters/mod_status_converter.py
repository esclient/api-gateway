from collections.abc import Mapping
from enum import Enum
from typing import Final

from gateway.stubs.mod_pb2 import ModStatus as ProtoModStatus


class GraphQLModStatus(str, Enum):
    UNSPECIFIED = "MOD_STATUS_UNSPECIFIED"
    UPLOADED = "MOD_STATUS_UPLOADED"
    BANNED = "MOD_STATUS_BANNED"
    HIDDEN = "MOD_STATUS_HIDDEN"


GRAPHQL_TO_PROTO: Final[Mapping[str, int]] = {
    GraphQLModStatus.UNSPECIFIED.value: ProtoModStatus.MOD_STATUS_UNSPECIFIED,
    GraphQLModStatus.UPLOADED.value: ProtoModStatus.MOD_STATUS_UPLOADED,
    GraphQLModStatus.BANNED.value: ProtoModStatus.MOD_STATUS_BANNED,
    GraphQLModStatus.HIDDEN.value: ProtoModStatus.MOD_STATUS_HIDDEN,
}

PROTO_TO_GRAPHQL: Final[Mapping[int, str]] = {v: k for k, v in GRAPHQL_TO_PROTO.items()}

DEFAULT_GRAPHQL: Final[str] = GraphQLModStatus.UNSPECIFIED.value
DEFAULT_PROTO: Final[int] = GRAPHQL_TO_PROTO[DEFAULT_GRAPHQL]


def graphql_to_proto_mod_status(graphql_value: str) -> int:
    return GRAPHQL_TO_PROTO.get(graphql_value, DEFAULT_PROTO)


def proto_to_graphql_mod_status(proto_value: int) -> str:
    return PROTO_TO_GRAPHQL.get(proto_value, DEFAULT_GRAPHQL)
