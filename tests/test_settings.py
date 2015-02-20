import pytest

from models import TestModel
from django.conf import settings
import actionitems.settings as actionitems_settings

class TestOriginModel:

    def test_origin_model_1_when_none_set_check_use(self):
        assert actionitems_settings.USE_ORIGIN_MODEL is False

    def test_origin_model_2_when_none_set_check_origin_model(self):
        assert actionitems_settings.ORIGIN_MODEL is None

    @pytest.mark.run_with_origin
    def test_origin_model_3_when_set_check_use(self):
        assert actionitems_settings.USE_ORIGIN_MODEL is not False

    @pytest.mark.run_with_origin
    def test_origin_model_4_when_set_check_origin_model(self):
        assert actionitems_settings.ORIGIN_MODEL == 'tests.TestModel'


class TestManagerList:
    def test_manager_list_1_check_default(self):
        assert actionitems_settings.MANAGER_LIST == (('internal', 'Internal'),)
