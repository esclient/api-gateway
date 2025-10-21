import pytest

from apigateway.converters.mod_status_converter import (
    DEFAULT_GRAPHQL,
    DEFAULT_PROTO,
    GRAPHQL_TO_PROTO,
    PROTO_TO_GRAPHQL,
    graphql_to_proto_mod_status,
    proto_to_graphql_mod_status,
)


@pytest.mark.parametrize("graphql_value", list(GRAPHQL_TO_PROTO))
def test_graphql_to_proto_known_values(graphql_value: str) -> None:
    assert graphql_to_proto_mod_status(graphql_value) == GRAPHQL_TO_PROTO[graphql_value]


def test_graphql_to_proto_defaults_to_unspecified() -> None:
    assert graphql_to_proto_mod_status("UNKNOWN") == DEFAULT_PROTO


@pytest.mark.parametrize("proto_value", list(PROTO_TO_GRAPHQL))
def test_proto_to_graphql_known_values(proto_value: int) -> None:
    assert proto_to_graphql_mod_status(proto_value) == PROTO_TO_GRAPHQL[proto_value]


def test_proto_to_graphql_defaults_to_unspecified() -> None:
    assert proto_to_graphql_mod_status(-1) == DEFAULT_GRAPHQL
