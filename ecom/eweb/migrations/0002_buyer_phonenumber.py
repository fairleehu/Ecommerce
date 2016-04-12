# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eweb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='phonenumber',
            field=models.CharField(default=0, max_length=11),
            preserve_default=False,
        ),
    ]
