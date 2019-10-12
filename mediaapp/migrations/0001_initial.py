# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MCCIABanner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_files', models.FileField(max_length=500, null=True, upload_to=b'printmedia/', blank=True)),
                ('banner_link', models.TextField(null=True)),
                ('is_expired', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('expire_date', models.DateTimeField(null=True, blank=True)),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.CharField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MCCIALEADERSHIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('leader_designation', models.CharField(max_length=200, null=True)),
                ('leader_name', models.CharField(max_length=200, null=True)),
                ('leader_post', models.CharField(max_length=200, null=True)),
                ('leader_organisation', models.CharField(max_length=200, null=True)),
                ('created_by', models.CharField(max_length=80, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='MCCIALinkToShare',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_files', models.FileField(max_length=500, null=True, upload_to=b'printmedia/', blank=True)),
                ('link_to_share', models.TextField(null=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.CharField(max_length=500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MCCIATeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member_designation', models.CharField(max_length=200, null=True)),
                ('member_name', models.CharField(max_length=200, null=True)),
                ('member_post', models.CharField(max_length=200, null=True)),
                ('created_by', models.CharField(max_length=80, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='MCCIATeamImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('document_files', models.FileField(max_length=500, null=True, upload_to=b'printmedia/', blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('creation_date', models.DateTimeField(null=True, blank=True)),
                ('created_by', models.CharField(max_length=500, null=True, blank=True)),
                ('leader_id', models.ForeignKey(blank=True, to='mediaapp.MCCIALEADERSHIP', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MCCIAVideoLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video_link', models.CharField(max_length=200, null=True)),
                ('video_type', models.CharField(max_length=200, null=True)),
                ('created_by', models.CharField(max_length=80, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
    ]
