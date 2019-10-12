# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
        ('membershipapp', '0001_initial'),
        ('eventsapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company_name', models.CharField(max_length=200, null=True, blank=True)),
                ('company_scale', models.CharField(default=b'MR', max_length=2, choices=[(b'MR', b'Micro'), (b'SM', b'Small'), (b'MD', b'Medium'), (b'LR', b'Large')])),
                ('gst', models.CharField(max_length=50, null=True, blank=True)),
                ('enroll_type', models.CharField(default=b'CO', max_length=2, choices=[(b'CO', b'Company'), (b'IN', b'Individual')])),
                ('is_member', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('membership_no', models.CharField(max_length=30, null=True, blank=True)),
                ('is_mccia', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('created_by', models.CharField(max_length=100, null=True, blank=True)),
                ('updated_by', models.CharField(max_length=100, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('industrydescription', models.ManyToManyField(related_name='industrydescription', to='adminapp.IndustryDescription', blank=True)),
                ('userdetail', models.ForeignKey(blank=True, to='membershipapp.UserDetail', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.EmailField(max_length=80, null=True, blank=True)),
                ('designation', models.CharField(max_length=50, null=True, blank=True)),
                ('cellno', models.CharField(max_length=50, null=True, blank=True)),
                ('hash_tag', models.TextField(null=True, blank=True)),
                ('is_member', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('is_mccia_person', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('interested_area', models.TextField(null=True, blank=True)),
                ('created_by', models.CharField(max_length=100, blank=True)),
                ('updated_by', models.CharField(max_length=100, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('companydetail', models.ForeignKey(blank=True, to='membershipapp.CompanyDetail', null=True)),
                ('nonmemberdetail', models.ForeignKey(blank=True, to='membershipapp.NonMemberDetail', null=True)),
                ('userdetail', models.ForeignKey(blank=True, to='membershipapp.UserDetail', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.EmailField(max_length=80, null=True, blank=True)),
                ('extra_email', models.TextField(null=True, blank=True)),
                ('designation', models.CharField(max_length=50, null=True, blank=True)),
                ('cellno', models.CharField(max_length=50, null=True, blank=True)),
                ('hash_tag', models.TextField(null=True, blank=True)),
                ('is_member', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('is_mccia_person', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('created_by', models.CharField(max_length=100, blank=True)),
                ('updated_by', models.CharField(max_length=100, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(null=True, blank=True)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('companydetail', models.ForeignKey(blank=True, to='massmailingapp.CompanyDetail', null=True)),
                ('eventdetail', models.ManyToManyField(to='eventsapp.EventDetails', blank=True)),
            ],
        ),
    ]
