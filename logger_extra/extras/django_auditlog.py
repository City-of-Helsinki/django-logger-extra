from functools import cache

from django.db.models import Model
from django.db.models.signals import pre_save

from logger_extra.logger_context import get_logger_context
from logger_extra.utils import json_serialize

DISPATCH_UID = "LoggerExtraDjangoAuditlog"


def enable_django_auditlog_augment() -> bool:
    """
    Attempts to augment django-auditlog entries with logger context.

    Returns:
        bool: True if auditlog was found and the signal connected, False otherwise.
    """
    has_auditlog, log_entry = _parse_audit_log_model()

    if not has_auditlog:
        return False

    pre_save.connect(
        _augment_django_auditlog,
        sender=log_entry,
        weak=False,
        dispatch_uid=DISPATCH_UID,
    )

    return True


def disable_django_auditlog_augment() -> bool:
    """
    Attempts to disconnect the django-auditlog entry augmentation if it's configured.
    """
    has_auditlog, log_entry = _parse_audit_log_model()

    if not has_auditlog:
        return False

    pre_save.disconnect(
        _augment_django_auditlog,
        sender=log_entry,
        dispatch_uid=DISPATCH_UID,
    )
    return True


def _augment_django_auditlog(sender: type[Model], instance: Model, **kwargs):
    has_auditlog, log_entry = _parse_audit_log_model()

    if not has_auditlog or sender != log_entry or not isinstance(instance, log_entry):
        return

    context = get_logger_context()

    if not hasattr(instance, "additional_data") or not isinstance(
        instance.additional_data, dict
    ):
        instance.additional_data = {}

    for key, value in context.items():
        instance.additional_data[key] = json_serialize(value)


@cache
def _parse_audit_log_model() -> tuple[bool, type[Model]]:
    try:
        from auditlog.models import LogEntry

        return (True, LogEntry)
    except ImportError:
        return (False, Model)
