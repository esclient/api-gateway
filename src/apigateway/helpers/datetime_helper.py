from datetime import UTC, datetime

from google.protobuf.timestamp_pb2 import Timestamp


def timestamp_to_datetime(timestamp: Timestamp) -> datetime | None:
    if timestamp.seconds == 0 and timestamp.nanos == 0:
        return None

    return timestamp.ToDatetime(tzinfo=UTC)
