# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeApi', '0003_homeadmin_nick'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='address',
            field=models.CharField(default=b'', max_length=100),
            preserve_default=True,
        ),
    ]
