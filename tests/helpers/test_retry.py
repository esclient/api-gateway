import logging
from types import SimpleNamespace

import grpc
import pytest
from faker import Faker

from apigateway.helpers.retry import (
    NON_RETRYABLE,
    RETRY_ATTEMPTS,
    grpc_retry,
    is_retryable_grpc_exception,
    log_retry_attempt,
)


class _FakeRpcError(grpc.RpcError):
    def __init__(self, status_code: grpc.StatusCode) -> None:
        super().__init__()
        self._status_code = status_code

    def code(self) -> grpc.StatusCode:  # type: ignore[override]
        return self._status_code


def test_is_retryable_grpc_exception_respects_non_retryable_codes() -> None:
    for code in NON_RETRYABLE:
        assert not is_retryable_grpc_exception(_FakeRpcError(code))

    assert is_retryable_grpc_exception(_FakeRpcError(grpc.StatusCode.UNAVAILABLE))


def test_log_retry_attempt_emits_warning_for_failed_retry(caplog: pytest.LogCaptureFixture, faker: Faker) -> None:
    error_message = faker.sentence(nb_words=3)
    exc = RuntimeError(error_message)
    attempt_number = faker.random_int(min=1, max=RETRY_ATTEMPTS)
    outcome = SimpleNamespace(failed=True, exception=lambda: exc)
    retry_state = SimpleNamespace(
        attempt_number=attempt_number,
        outcome=outcome,
        next_action=SimpleNamespace(sleep=faker.pyfloat(min_value=0.1, max_value=2.0)),
    )

    caplog.set_level(logging.WARNING)
    log_retry_attempt(retry_state)

    assert caplog.records
    assert f"{attempt_number}/{RETRY_ATTEMPTS}" in caplog.records[0].message
    assert error_message in caplog.records[0].message


def test_grpc_retry_retries_retryable_errors() -> None:
    attempts = 0

    @grpc_retry()
    def flaky_call() -> None:
        nonlocal attempts
        attempts += 1
        raise _FakeRpcError(grpc.StatusCode.ABORTED)

    with pytest.raises(_FakeRpcError):
        flaky_call()

    assert attempts == RETRY_ATTEMPTS
