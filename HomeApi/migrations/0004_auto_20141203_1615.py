# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeApi', '0003_auto_20141202_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='block',
            name='lat',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='block',
            name='lng',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
