import logging
from unittest.mock import MagicMock, patch

import pytest
from sentry_sdk.integrations.logging import SentryHandler

from logger_extra.extras.django_auditlog import (
    disable_django_auditlog_augment,
    enable_django_auditlog_augment,
)
from logger_extra.extras.sentry import (
    attach_sentry_handler,
    detach_sentry_handler,
)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    yield
    disable_django_auditlog_augment()


def test_auditlog_present():
    with patch("logger_extra.extras.django_auditlog.has_auditlog", True):
        assert enable_django_auditlog_augment()


def test_auditlog_missing():
    with patch("logger_extra.extras.django_auditlog.has_auditlog", False):
        assert not enable_django_auditlog_augment()


def test_sentry_present_and_active():
    logger = logging.getLogger(__name__)
    mock_client = MagicMock()
    mock_client.is_active.return_value = True

    with (
        patch("logger_extra.extras.sentry.get_sentry_client", return_value=mock_client),
        patch("logger_extra.extras.sentry.has_sentry", True),
    ):
        assert attach_sentry_handler(logger)
        assert attach_sentry_handler(logger)

        num_sentry_handlers = sum(
            1 for h in logger.handlers if isinstance(h, SentryHandler)
        )

        assert num_sentry_handlers == 1
        assert detach_sentry_handler(logger)
        assert not detach_sentry_handler(logger)


def test_sentry_present_and_inactive():
    logger = logging.getLogger(__name__)
    mock_client = MagicMock()
    mock_client.is_active.return_value = False

    with (
        patch("logger_extra.extras.sentry.has_sentry", True),
        patch("logger_extra.extras.sentry.get_sentry_client", return_value=mock_client),
    ):
        assert not attach_sentry_handler(logger)
        assert not detach_sentry_handler(logger)


def test_sentry_missing():
    logger = logging.getLogger(__name__)

    with patch("logger_extra.extras.sentry.has_sentry", False):
        assert not attach_sentry_handler(logger)
        assert not detach_sentry_handler(logger)


def test_sentry_throws_on_attach():
    logger = logging.getLogger(__name__)
    mock_client = MagicMock()
    mock_client.is_active.side_effect = Exception()

    with (
        patch("logger_extra.extras.sentry.get_sentry_client", return_value=mock_client),
        patch("logger_extra.extras.sentry.has_sentry", True),
    ):
        assert not attach_sentry_handler(logger)


def test_sentry_throws_on_detach():
    handler = SentryHandler()

    logger = MagicMock()
    logger.handlers = [handler]
    logger.removeHandler.side_effect = Exception()

    mock_client = MagicMock()
    mock_client.is_active.return_value = True

    with (
        patch("logger_extra.extras.sentry.get_sentry_client", return_value=mock_client),
        patch("logger_extra.extras.sentry.has_sentry", True),
    ):
        assert not detach_sentry_handler(logger)
