# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('backofficeapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publication_type', models.IntegerField(default=0, choices=[(0, b'Sampada'), (1, b'Annual Report'), (2, b'World of Business')])),
                ('file_path', models.ImageField(null=True, upload_to=b'Publication/Publication_File', blank=True)),
                ('cover_path', models.ImageField(null=True, upload_to=b'Publication/CoverImages', blank=True)),
                ('publish_date', models.DateField(null=True, blank=True)),
                ('volume_no', models.CharField(max_length=20, null=True, blank=True)),
                ('issue_no', models.CharField(max_length=20, null=True, blank=True)),
                ('created_by', models.CharField(max_length=100, null=True, blank=True)),
                ('updated_by', models.CharField(max_length=100, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('contact_person', models.ForeignKey(blank=True, to='backofficeapp.SystemUserProfile', null=True)),
            ],
        ),
    ]
