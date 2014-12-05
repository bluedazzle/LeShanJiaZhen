# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeApi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneverify',
            name='phone',
            field=models.CharField(max_length=11),
        ),
    ]
