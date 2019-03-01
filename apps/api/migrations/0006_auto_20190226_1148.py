# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-26 11:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userminiprofile',
            name='page_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='api.Page'),
        ),
    ]