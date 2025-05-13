import logging

from django.apps import apps
from django.conf import settings

from logger_extra.extras.django_auditlog import (
    augment_django_auditlog,
)

logger = logging.getLogger(__name__)


def configure_django_auditlog():
    augment_enabled = getattr(settings, "LOGGER_EXTRA_AUGMENT_DJANGO_AUDITLOG", False)
    auditlog_installed = apps.is_installed("auditlog")

    if augment_enabled:
        if not auditlog_installed:
            logger.warning("django-auditlog is not installed.")
            return False

        if not augment_django_auditlog():
            logger.error("failed to augment django-auditlog.")
            return False

        return True

    return False
