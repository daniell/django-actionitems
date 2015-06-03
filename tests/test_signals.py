import pytest

from mock import patch

from actionitems.models import ActionItem


class TestSignalSentWhenModelSaved(object):
    @patch('actionitems.models.done_status_changed')
    def test_signal_for_done_status_changed_sent_when_new_item_is_done(self, signal_sent):
        action_item = ActionItem(done=True)
        action_item.save()
        assert signal_sent.send.called

    @patch('actionitems.models.done_status_changed')
    def test_signal_for_done_status_changed_sent_when_done_is_set(self, signal_sent):
        action_item = ActionItem.objects.create()
        action_item.done = True
        action_item.save()
        assert signal_sent.send.called

    @patch('actionitems.models.done_status_changed')
    def test_signal_for_done_status_changed_sent_when_done_is_unset(self, signal_sent):
        action_item = ActionItem.objects.create(done=True)
        action_item.done = False
        action_item.save()
        assert signal_sent.send.called

    @patch('actionitems.models.done_status_changed')
    def test_signal_for_done_status_changed_not_sent_when_done_status_remains_set(self, signal_sent):
        action_item = ActionItem.objects.create(done=True)
        action_item.done = True
        action_item.save()
        assert not signal_sent.send.called

    @patch('actionitems.models.done_status_changed')
    def test_signal_for_done_status_changed_not_sent_when_done_status_remains_unset(self, signal_sent):
        action_item = ActionItem.objects.create(done=False)
        action_item.done = False
        action_item.save()
        assert not signal_sent.send.called

    @patch('actionitems.models.done_status_changed')
    def test_signal_for_done_status_changed_not_sent_when_new_item_isnt_done(self, signal_sent):
        action_item = ActionItem(done=False)
        action_item.save()
        assert not signal_sent.send.called
