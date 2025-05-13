from typing import Type

from django.db.models.signals import pre_save

from logger_extra.logger_context import get_logger_context
from logger_extra.utils import json_serialize


def augment_django_auditlog():
    try:
        from auditlog.models import LogEntry

        def _augment_django_auditlog(
                sender: Type[LogEntry],
                instance: LogEntry,
                **kwargs
        ):
            if sender != LogEntry or not isinstance(instance, LogEntry):
                return False

            context = get_logger_context()

            if not instance.additional_data:
                instance.additional_data = {}

            for key, value in context.items():
                instance.additional_data[key] = json_serialize(value)

        pre_save.connect(_augment_django_auditlog, sender=LogEntry, weak=False)
        return True
    except ImportError:
        return False



