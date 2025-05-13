from unittest import mock

from django.test import TestCase

from logger_extra.extras.django_auditlog import (
    _parse_audit_log_model,
    enable_django_auditlog_augment,
)


class ExtrasTestCase(TestCase):
    def setUp(self):
        _parse_audit_log_model.cache_clear()

    def test_auditlog_present(self):
        assert enable_django_auditlog_augment()

    def test_auditlog_missing(self):
        with mock.patch.dict("sys.modules", {"auditlog.models": None}):
            assert not enable_django_auditlog_augment()
