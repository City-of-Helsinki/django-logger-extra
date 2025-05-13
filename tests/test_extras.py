from importlib import reload
from unittest import mock

from django.test import TestCase

import logger_extra.extras.django_auditlog as django_auditlog


class ExtrasTestCase(TestCase):
    def test_auditlog_present(self):
        assert django_auditlog.enable_django_auditlog_augment()

    def test_auditlog_missing(self):
        with mock.patch.dict("sys.modules", {"auditlog.models": None}):
            # Need to reload the module to force reload of dynamic import
            reload(django_auditlog)
            assert not django_auditlog.enable_django_auditlog_augment()
