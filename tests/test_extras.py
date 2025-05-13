from unittest import mock

from django.test import TestCase, override_settings

from logger_extra.extras.configure import configure_django_auditlog


class ExtrasTestCase(TestCase):
    @override_settings(LOGGER_EXTRA_AUGMENT_DJANGO_AUDITLOG=True)
    def test_configure_enabled_auditlog_present(self):
        assert configure_django_auditlog()

    @override_settings(LOGGER_EXTRA_AUGMENT_DJANGO_AUDITLOG=False)
    def test_configure_disabled_auditlog_present(self):
        assert not configure_django_auditlog()

    @override_settings(LOGGER_EXTRA_AUGMENT_DJANGO_AUDITLOG=True)
    def test_configure_enabled_django_auditlog_missing(self):
        with mock.patch.dict("sys.modules", {"auditlog.models": None}):
            assert not configure_django_auditlog()
