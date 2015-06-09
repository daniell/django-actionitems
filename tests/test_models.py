import pytest
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.core import management
from django.conf import settings

from helpers import random_string, random_date
from actionitems.models import ActionItem
from models import TestModel

class TestHandleDone(object):
    def test_handle_done_1_with_done_null(self):
        # With actionitem.done not set, completed on should be empty
        actionitem = ActionItem()
        actionitem.handle_done()
        assert actionitem.completed_on is None

    def test_handle_done_2_with_done_null_when_completed_on_has_initial_value(self):
        # With actionitem.done not set, completed on should be forced empty
        actionitem = ActionItem()
        actionitem.completed_on = random_date()
        actionitem.handle_done()
        assert actionitem.completed_on is None

    def test_handle_done_3_with_done_set_when_completed_on_has_not_been_set(self):
        # With actionitem.done set, completed on should be set
        actionitem = ActionItem()
        actionitem.done = True
        actionitem.handle_done()
        delta = actionitem.completed_on - datetime.utcnow().replace(tzinfo=utc)
        assert abs(delta) <= timedelta(milliseconds=10), 'Times are not almost equal'

    def test_handle_done_4_with_done_set_false_removes_completed_on(self):
        # Completed on should be removed if done is false
        actionitem = ActionItem()
        actionitem.completed_on = random_date()
        actionitem.handle_done()
        assert actionitem.completed_on is None

    def test_handle_done_5_with_done_true_and_completed_on_in_past_that_completed_on_remains(self):
        # Completed on shouldn't change if nothing has changed
        actionitem = ActionItem()
        actionitem.completed_on = completed_on = random_date()
        actionitem.done = True
        actionitem.handle_done()
        assert actionitem.completed_on == completed_on


class TestSave(object):

    # NB Model.objects.create() is a convenience method for creating an object and saving it all in one step.
    @pytest.mark.django_db
    def test_save_1_confirm_that_handle_done_result_is_saved_with_done_true(self):
        actionitem = ActionItem.objects.create(done=True)
        assert actionitem.completed_on is not None


class TestTitle(object):

    def test_title_1_with_short_description(self):
        description = random_string(30)
        actionitem = ActionItem()
        actionitem.description = description
        assert actionitem.title() == description

    def test_title_2_with_long_description_with_default(self):
        description = random_string(1000)
        actionitem = ActionItem()
        actionitem.description = description
        assert actionitem.title() == description[:140]


class TestOriginModel(object):

    def test_origin_model_1_origin_not_present_if_origin_not_used(self):
        with pytest.raises(AttributeError):
            ActionItem().origin

    @pytest.mark.django_db
    @pytest.mark.run_with_origin
    def test_origin_model_2(self):
        testitem1 = TestModel.objects.create()
        actionitem2 = ActionItem.objects.create(origin=testitem1)
        assert actionitem2.origin.pk == testitem1.pk
