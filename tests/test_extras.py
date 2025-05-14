from unittest import mock

from django.test import TestCase

from logger_extra.extras.django_auditlog import (
    disable_django_auditlog_augment,
    enable_django_auditlog_augment,
)


class ExtrasTestCase(TestCase):
    def tearDown(self):
        disable_django_auditlog_augment()
        return super().tearDown()

    def test_auditlog_present(self):
        assert enable_django_auditlog_augment()

    @mock.patch("logger_extra.extras.django_auditlog.has_auditlog", False)
    def test_auditlog_missing(self):
        assert not enable_django_auditlog_augment()
