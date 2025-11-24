from datetime import UTC, datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp

from apigateway.helpers.datetime_helper import timestamp_to_datetime


def test_raises_for_none_input() -> None:
    with pytest.raises(AttributeError):
        timestamp_to_datetime(None)  # type: ignore[arg-type]


def test_returns_none_for_empty_timestamp() -> None:
    assert timestamp_to_datetime(Timestamp()) is None


def test_converts_timestamp_to_datetime_with_utc() -> None:
    dt = datetime(2024, 5, 6, 7, 8, 9, tzinfo=UTC)
    ts = Timestamp()
    ts.FromDatetime(dt)

    assert timestamp_to_datetime(ts) == dt


def test_naive_datetime_gets_utc_attached() -> None:
    naive_dt = datetime(2024, 5, 6, 7, 8, 9)
    ts = Timestamp()
    ts.FromDatetime(naive_dt)

    result = timestamp_to_datetime(ts)

    assert result == naive_dt.replace(tzinfo=UTC)
    assert result.tzinfo is UTC


def test_timezone_aware_datetime_passthrough() -> None:
    aware_dt = datetime(2024, 5, 6, 7, 8, 9, tzinfo=UTC)
    ts = Timestamp()
    ts.FromDatetime(aware_dt)

    result = timestamp_to_datetime(ts)

    assert result == aware_dt
    assert result.tzinfo is UTC


def test_raises_for_unsupported_type() -> None:
    with pytest.raises(AttributeError):
        timestamp_to_datetime("2024-05-06T07:08:09Z")  # type: ignore[arg-type]
