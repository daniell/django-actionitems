from django.utils import timezone

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
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(null=True, blank=True)
    manager = models.CharField(max_length=10, choices=MANAGER_LIST, default=MANAGER_LIST[0][0])

    # USE_ORIGIN_MODEL and ORIGIN_MODEL come from actionitems.settings
    if USE_ORIGIN_MODEL:
        origin = models.ForeignKey(ORIGIN_MODEL, null=True, blank=True)

    def handle_done(self):
        self.handle_done_status_change()
        if not self.done:
            self.completed_on = None
        if self.done and not self.completed_on:
            self.completed_on = timezone.now()

    def handle_done_status_change(self):
        if not self.pk and self.done:
            done_status_changed.send(self)
        elif self.pk:
            old_action_item = ActionItem.objects.get(pk=self.id)
            if old_action_item.done != self.done:
                done_status_changed.send(self)

    def save(self, *args, **kwargs):
        self.handle_done()
        super(ActionItem, self).save(*args, **kwargs)

    def title(self):
        description = strip_tags(self.description)
        return description[:140]
