# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=500, null=True, blank=True)),
                ('photo', models.CharField(max_length=50, null=True, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('is_new', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('old_area_id', models.IntegerField()),
                ('new_area_id', models.IntegerField()),
                ('apply_time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(max_length=2)),
                ('photo', models.CharField(max_length=100, null=True, blank=True)),
                ('address', models.CharField(default=b'', max_length=100)),
                ('name', models.CharField(default=b'', max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('area_id', models.IntegerField(unique=True)),
                ('area_name', models.CharField(max_length=10)),
                ('area_tel', models.CharField(max_length=20)),
                ('area_info', models.CharField(max_length=1000, null=True, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('lat', models.FloatField(null=True)),
                ('lng', models.FloatField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=15)),
                ('verified', models.BooleanField(default=False)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomeAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(max_length=50)),
                ('nick', models.CharField(default=b'', max_length=50)),
                ('log_time', models.DateTimeField(max_length=20)),
                ('reg_time', models.DateTimeField(auto_now_add=True)),
                ('type', models.IntegerField(default=1, max_length=2)),
                ('verify', models.BooleanField(default=False)),
                ('work_num', models.CharField(max_length=50, null=True, blank=True)),
                ('area', models.ForeignKey(blank=True, to='HomeApi.Block', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomeItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=500)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomeItem_O',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.CharField(max_length=50)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='HomeItem_P',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_name', models.CharField(max_length=10)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneVerify',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=11)),
                ('verify', models.IntegerField(max_length=10)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='homeitem_o',
            name='parent_item',
            field=models.ForeignKey(to='HomeApi.HomeItem_P'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homeitem',
            name='parent_item',
            field=models.ForeignKey(blank=True, to='HomeApi.HomeItem_O', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='area',
            field=models.ForeignKey(to='HomeApi.Block'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='consumer',
            field=models.ForeignKey(to='HomeApi.Consumer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='appointment',
            name='process_by',
            field=models.ForeignKey(blank=True, to='HomeApi.HomeAdmin', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='application',
            name='apply_user',
            field=models.ForeignKey(to='HomeApi.HomeAdmin'),
            preserve_default=True,
        ),
    ]
