from datetime import UTC, datetime

from ariadne import ScalarType

datetime_scalar = ScalarType("DateTime")


@datetime_scalar.serializer
def serialize_datetime(value: datetime | str) -> str:
    if isinstance(value, str):
        return value

    if not isinstance(value, datetime):
        raise TypeError("DateTime value must be datetime or ISO string")

    if value.tzinfo is None:
        value = value.replace(tzinfo=UTC)

    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value: str) -> datetime:
    if not isinstance(value, str):
        raise TypeError("DateTime value must be a string")

    normalized = value if not value.endswith("Z") else value[:-1] + "+00:00"
    return datetime.fromisoformat(normalized)
