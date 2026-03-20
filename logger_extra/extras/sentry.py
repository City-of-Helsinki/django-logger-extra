import logging

try:
    from sentry_sdk import get_client as get_sentry_client
    from sentry_sdk.integrations.logging import SentryHandler

    has_sentry = True
except ImportError:
    get_sentry_client = None
    SentryHandler = None
    has_sentry = False


def attach_sentry_handler(logger: logging.Logger) -> bool:
    if not has_sentry or not get_sentry_client:
        return False

    try:
        client = get_sentry_client()

        if not client or not client.is_active():
            return False

        if any(isinstance(h, SentryHandler) for h in logger.handlers):
            return True  # Already configured

        sentry_handler = SentryHandler()
        sentry_handler.setLevel(logging.ERROR)

        logger.addHandler(sentry_handler)
        return True
    except Exception:
        return False


def detach_sentry_handler(logger: logging.Logger) -> bool:
    if not has_sentry:
        return False

    try:
        handler = next(
            (h for h in logger.handlers if isinstance(h, SentryHandler)), None
        )

        if not handler:
            return False

        handler.close()
        logger.removeHandler(handler)
        return True
    except Exception:
        return False
