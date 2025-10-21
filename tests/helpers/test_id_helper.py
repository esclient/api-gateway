import pytest
from faker import Faker
from graphql import GraphQLError

from apigateway.helpers.id_helper import validate_and_convert_id


def test_validate_and_convert_id_returns_int_for_valid_string(faker: Faker) -> None:
    numeric_value = faker.random_int(min=1)
    raw_id = str(numeric_value)

    assert validate_and_convert_id(raw_id) == numeric_value


def test_validate_and_convert_id_trims_whitespace(faker: Faker) -> None:
    numeric_value = faker.random_int(min=1)
    raw_id = f"\t{numeric_value}\n"

    assert validate_and_convert_id(raw_id) == numeric_value


def test_validate_and_convert_id_raises_for_empty_input(faker: Faker) -> None:
    field_name = faker.word()

    with pytest.raises(GraphQLError) as exc:
        validate_and_convert_id(" ", field_name=field_name)

    assert exc.value.extensions == {"code": "MISSING_ID", "field": field_name}


def test_validate_and_convert_id_raises_for_non_numeric(faker: Faker) -> None:
    field_name = faker.word()
    invalid_value = faker.lexify(text="??????")

    with pytest.raises(GraphQLError) as exc:
        validate_and_convert_id(invalid_value, field_name=field_name)

    assert exc.value.extensions == {
        "code": "INVALID_ID_FORMAT",
        "field": field_name,
        "value": invalid_value,
    }
