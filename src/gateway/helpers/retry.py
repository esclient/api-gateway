import logging

import grpc
from tenacity import RetryCallState, retry, retry_if_exception, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

NON_RETRYABLE = {grpc.StatusCode.UNIMPLEMENTED, grpc.StatusCode.INVALID_ARGUMENT, grpc.StatusCode.NOT_FOUND}

RETRY_ATTEMPTS = 3
RETRY_DELAY_MULTIPLIER = 1
RETRY_DELAY_MIN = 1
RETRY_DELAY_MAX = 10


def is_retryable_grpc_exception(exc: BaseException) -> bool:
    if isinstance(exc, grpc.RpcError):
        code = exc.code() if hasattr(exc, "code") else None
        return code not in NON_RETRYABLE
    return False


def log_retry_attempt(retry_state: RetryCallState) -> None:
    if retry_state.attempt_number < 1:
        return

    if retry_state.outcome is None or not retry_state.outcome.failed or not hasattr(retry_state.outcome, "exception"):
        return

    try:
        exception = retry_state.outcome.exception()
        if exception is None:
            return

        sleep_time = getattr(retry_state.next_action, "sleep", 0) if retry_state.next_action else 0

        logger.warning(
            f"Повторная попытка {retry_state.attempt_number}/{RETRY_ATTEMPTS} "
            f"для gRPC вызова. Ошибка: {exception} "
            f"(следующая попытка через {sleep_time:.1f} сек)"
        )
    except Exception as e:
        logger.debug(f"Ошибка при логировании повторной попытки: {e}")


def grpc_retry():  # type: ignore
    return retry(
        stop=stop_after_attempt(RETRY_ATTEMPTS),
        wait=wait_exponential(multiplier=RETRY_DELAY_MULTIPLIER, min=RETRY_DELAY_MIN, max=RETRY_DELAY_MAX),
        retry=retry_if_exception(is_retryable_grpc_exception),
        reraise=True,
        before_sleep=log_retry_attempt,
    )
