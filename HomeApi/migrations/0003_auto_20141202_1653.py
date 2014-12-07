# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HomeApi', '0002_homeitem_parent_item'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Advertisment',
            new_name='Advertisement',
        ),
    ]
