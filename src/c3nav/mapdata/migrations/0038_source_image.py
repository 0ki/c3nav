# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-01 14:41
from __future__ import unicode_literals

import os

from django.conf import settings
from django.db import migrations, models


def save_images_to_db(apps, schema_editor):
    Source = apps.get_model('mapdata', 'Source')
    for source in Source.objects.all():
        image_path = os.path.join(settings.MAP_ROOT, source.package.directory, 'sources', source.name)
        source.image = open(image_path, 'rb').read()
        source.save()


class Migration(migrations.Migration):
    dependencies = [
        ('mapdata', '0037_auto_20170428_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='image',
            field=models.BinaryField(default=b'', verbose_name='image data'),
            preserve_default=False,
        ),
        migrations.RunPython(save_images_to_db),
    ]