from datetime import datetime
from django.utils.timezone import utc

from django.utils.html import strip_tags
from django.db import models

from actionitems.settings import *
from actionitems.signals import done_status_changed


class ActionItem(models.Model):
    description = models.TextField()
    responsible = models.CharField(max_length=100)
    deadline = models.DateField(null=True, blank=True)
    completed_on = models.DateTimeField(null=True, blank=True, editable=False)
    done = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.utcnow().replace(tzinfo=utc))
    updated_on = models.DateTimeField(null=True, blank=True)
    manager = models.CharField(max_length=10, choices=MANAGER_LIST, default=MANAGER_LIST[0][0])

    # USE_ORIGIN_MODEL and ORIGIN_MODEL come from actionitems.settings
    if USE_ORIGIN_MODEL:
        origin = models.ForeignKey(ORIGIN_MODEL, null=True, blank=True)

    def handle_done(self, actionitem):
        self.handle_done_status_change()
        if not actionitem.done:
            actionitem.completed_on = None
        if actionitem.done and not actionitem.completed_on:
            actionitem.completed_on = datetime.utcnow().replace(tzinfo=utc)


    def handle_done_status_change(self):
        if not self.pk and self.done:
            done_status_changed.send(self)
        elif self.pk:
            old_action_item = ActionItem.objects.get(pk=self.id)
            if old_action_item.done != self.done:
                done_status_changed.send(self)

    def save(self, *args, **kwargs):
        self.handle_done(self)
        super(ActionItem, self).save(*args, **kwargs)

    def title(self):
        description = strip_tags(self.description)
        return description[:140]
