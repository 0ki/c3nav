# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 20:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('editor', '0012_remove_changeset_session_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changesetupdate',
            name='session_user',
        ),
    ]