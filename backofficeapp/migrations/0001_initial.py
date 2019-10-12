# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('department_name', models.CharField(max_length=250)),
                ('created_by', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designation_name', models.CharField(max_length=250)),
                ('created_by', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='SystemUserProfile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('contact_no', models.CharField(max_length=50)),
                ('type', models.CharField(default=b'WEB_USER', max_length=20, choices=[(b'SUPER_ADMIN', b'SUPER_ADMIN'), (b'WEB_USER', b'WEB_USER'), (b'MEMBER', b'MEMBER'), (b'EVENT', b'EVENT'), (b'ADMIN', b'ADMIN')])),
                ('user_status', models.CharField(default=b'ACTIVE', max_length=20, choices=[(b'ACTIVE', b'ACTIVE'), (b'INACTIVE', b'INACTIVE')])),
                ('user_type', models.CharField(blank=True, max_length=20, null=True, choices=[(b'SUPER_ADMIN', b'SUPER_ADMIN'), (b'WEB_USER', b'WEB_USER'), (b'MEMBER', b'MEMBER'), (b'EVENT', b'EVENT'), (b'ADMIN', b'ADMIN')])),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('created_by', models.CharField(max_length=500)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(null=True, blank=True)),
                ('updated_by', models.CharField(max_length=500, null=True, blank=True)),
                ('department', models.ForeignKey(blank=True, to='backofficeapp.Department', null=True)),
                ('designation', models.ForeignKey(blank=True, to='backofficeapp.Designation', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserPrivilege',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('privilege', models.CharField(max_length=500)),
                ('module_name', models.CharField(max_length=100, null=True, blank=True)),
                ('created_by', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('status', models.CharField(default=b'Active', max_length=20, choices=[(b'ACTIVE', b'ACTIVE'), (b'INACTIVE', b'INACTIVE')])),
                ('created_by', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('is_active', models.BooleanField(default=True, choices=[(True, True), (False, False)])),
                ('privilege', models.ManyToManyField(to='backofficeapp.UserPrivilege')),
            ],
        ),
        migrations.AddField(
            model_name='systemuserprofile',
            name='role',
            field=models.ForeignKey(blank=True, to='backofficeapp.UserRole', null=True),
        ),
    ]
