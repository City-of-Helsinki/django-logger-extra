import logging
from django.apps import AppConfig


logger = logging.getLogger(__name__)


class LoggerExtraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "logger_extra"

    def ready(self):
        try:
            from logger_extra.extras.django_auditlog import (
                augment_django_auditlog_extras,
            )

            augment_django_auditlog_extras()
        except ImportError:
            logger.warning(
                "Failed to import logger_extra.extras.django_auditlog, most likely django-auditlog is not installed."
            )
