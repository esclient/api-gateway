from gateway.stubs.mod_pb2 import ModStatus as ProtoMS
from enum import Enum


class GraphQLModStatus(str, Enum):
    UNSPECIFIED = "MOD_STATUS_UNSPECIFIED"
    UPLOADED = "MOD_STATUS_UPLOADED"
    BANNED = "MOD_STATUS_BANNED"
    HIDDEN = "MOD_STATUS_HIDDEN"


def graphql_to_proto_mod_status(graphql_value: str) -> int:
    mapping = {
        GraphQLModStatus.UNSPECIFIED: ProtoMS.MOD_STATUS_UNSPECIFIED,
        GraphQLModStatus.UPLOADED: ProtoMS.MOD_STATUS_UPLOADED,
        GraphQLModStatus.BANNED: ProtoMS.MOD_STATUS_BANNED,
        GraphQLModStatus.HIDDEN: ProtoMS.MOD_STATUS_HIDDEN,
    }
    return mapping.get(
        graphql_value, ProtoMS.MOD_STATUS_UNSPECIFIED
    )  # <Если получили непонятное значение. Пока пусть будет MOD_STATUS_UNSPECIFIED>#


def proto_to_graphql_mod_status(proto_value: int) -> str:
    mapping = {
        ProtoMS.MOD_STATUS_UNSPECIFIED: GraphQLModStatus.UNSPECIFIED,
        ProtoMS.MOD_STATUS_UPLOADED: GraphQLModStatus.UPLOADED,
        ProtoMS.MOD_STATUS_BANNED: GraphQLModStatus.BANNED,
        ProtoMS.MOD_STATUS_HIDDEN: GraphQLModStatus.HIDDEN,
    }
    return mapping.get(proto_value, GraphQLModStatus.UNSPECIFIED)
