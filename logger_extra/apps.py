import logging

from django.apps import AppConfig

from logger_extra.extras.configure import configure_django_auditlog

logger = logging.getLogger(__name__)


class LoggerExtraConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "logger_extra"

    def ready(self):
        configure_django_auditlog()
