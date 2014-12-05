# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeApi', '0002_auto_20141202_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeadmin',
            name='nick',
            field=models.CharField(default=b'', max_length=50),
            preserve_default=True,
        ),
    ]
