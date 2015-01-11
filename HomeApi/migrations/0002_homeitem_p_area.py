# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeApi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeitem_p',
            name='area',
            field=models.ForeignKey(blank=True, to='HomeApi.Block', null=True),
            preserve_default=True,
        ),
    ]
