import logging

from django.apps import AppConfig
from django.conf import settings

LIB_NAME = __package__
logger = logging.getLogger(LIB_NAME)


class LoggerExtraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "logger_extra"

    def ready(self):
        from logger_extra.extras.django_auditlog import enable_django_auditlog_augment
        from logger_extra.extras.sentry import attach_sentry_handler

        enable_sentry = getattr(settings, "LOGGER_EXTRA_USE_SENTRY", False)
        augment_enabled = getattr(
            settings, "LOGGER_EXTRA_AUGMENT_DJANGO_AUDITLOG", False
        )

        if enable_sentry and not attach_sentry_handler(logger):
            logger.error("failed to attach sentry handler.")

        if augment_enabled and not enable_django_auditlog_augment():
            logger.error("failed to augment django-auditlog.")
