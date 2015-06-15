# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActionItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField()),
                ('responsible', models.CharField(max_length=100)),
                ('deadline', models.DateField(null=True, blank=True)),
                ('completed_on', models.DateTimeField(null=True, editable=False, blank=True)),
                ('done', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(default=datetime.datetime(2015, 6, 15, 13, 41, 13, 545210, tzinfo=utc))),
                ('updated_on', models.DateTimeField(null=True, blank=True)),
                ('manager', models.CharField(default=b'internal', max_length=10, choices=[(b'internal', b'Internal')])),
            ],
        ),
    ]
