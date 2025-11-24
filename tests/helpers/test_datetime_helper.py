from datetime import UTC, datetime

import pytest
from google.protobuf.timestamp_pb2 import Timestamp

from apigateway.helpers.datetime_helper import timestamp_to_datetime


def test_returns_none_for_none() -> None:
    assert timestamp_to_datetime(None) is None


def test_returns_none_for_empty_timestamp() -> None:
    assert timestamp_to_datetime(Timestamp()) is None


def test_converts_timestamp_to_datetime_with_utc() -> None:
    dt = datetime(2024, 5, 6, 7, 8, 9, tzinfo=UTC)
    ts = Timestamp()
    ts.FromDatetime(dt)

    assert timestamp_to_datetime(ts) == dt


def test_naive_datetime_gets_utc_attached() -> None:
    naive_dt = datetime(2024, 5, 6, 7, 8, 9)

    result = timestamp_to_datetime(naive_dt)

    assert result == naive_dt.replace(tzinfo=UTC)


def test_timezone_aware_datetime_passthrough() -> None:
    aware_dt = datetime(2024, 5, 6, 7, 8, 9, tzinfo=UTC)

    assert timestamp_to_datetime(aware_dt) is aware_dt


def test_raises_for_unsupported_type() -> None:
    with pytest.raises(TypeError):
        timestamp_to_datetime("2024-05-06T07:08:09Z")  # type: ignore[arg-type]
