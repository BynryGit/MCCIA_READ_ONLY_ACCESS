# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
        ('hallbookingapp', '0001_initial'),
        ('membershipapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership_Visa_Recommendations',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('visa_recommendation_no', models.CharField(max_length=30, null=True, blank=True)),
                ('person_title', models.CharField(default=b'Mr.', max_length=3, choices=[(b'Mr.', b'Mr.'), (b'Mrs.', b'Mrs.'), (b'Ms.', b'Ms.')])),
                ('person_name', models.CharField(max_length=80, null=True, blank=True)),
                ('person_designation', models.CharField(max_length=70, blank=True)),
                ('mobile_no', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.CharField(max_length=90, blank=True)),
                ('purpose_to_visit', models.CharField(default=b'WV', max_length=10, choices=[(b'WV', b'Work Visit'), (b'BU', b'Business')])),
                ('visiting_from_date', models.DateField(default=django.utils.timezone.now, blank=True)),
                ('visa_type', models.CharField(default=b'Single', max_length=20, null=True, blank=True, choices=[(b'Single', b'Single Entry'), (b'Multiple', b'Multiple Entry')])),
                ('radio_choice', models.CharField(default=b'Day', max_length=20, null=True, blank=True, choices=[(b'Day', b'Day'), (b'Week', b'Week'), (b'Month', b'Month')])),
                ('visitDurations', models.CharField(max_length=80, null=True, blank=True)),
                ('total_visit_durations', models.CharField(max_length=80, null=True, blank=True)),
                ('passport_no', models.CharField(max_length=30, null=True, blank=True)),
                ('passport_valid_from_date', models.DateField(default=django.utils.timezone.now, blank=True)),
                ('passport_valid_to_date', models.DateField(default=django.utils.timezone.now, blank=True)),
                ('company_name', models.CharField(max_length=80, null=True, blank=True)),
                ('address', models.TextField(null=True)),
                ('passport_copy', models.CharField(default=b'NO', max_length=20, null=True, blank=True, choices=[(b'YES', b'YES'), (b'NO', b'NO')])),
                ('doc_file', models.FileField(null=True, upload_to=b'DOC_PATH', blank=True)),
                ('created_by', models.CharField(max_length=80, null=True, blank=True)),
                ('updated_by', models.CharField(max_length=80, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(null=True, blank=True)),
                ('is_completed', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('location', models.ForeignKey(blank=True, to='hallbookingapp.HallLocation', null=True)),
                ('mcciamember', models.ForeignKey(blank=True, to='membershipapp.UserDetail', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceOfEmbassy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('embassy_name', models.CharField(max_length=150, null=True, blank=True)),
                ('address', models.CharField(max_length=500, null=True, blank=True)),
                ('city', models.CharField(max_length=60, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_deleted', models.BooleanField(default=False, choices=[(True, True), (False, False)])),
                ('country', models.ForeignKey(blank=True, to='adminapp.Country', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='membership_visa_recommendations',
            name='place_of_embassy',
            field=models.ForeignKey(blank=True, to='visarecommendationapp.PlaceOfEmbassy', null=True),
        ),
        migrations.AddField(
            model_name='membership_visa_recommendations',
            name='to_which_country',
            field=models.ForeignKey(blank=True, to='adminapp.Country', null=True),
        ),
    ]
