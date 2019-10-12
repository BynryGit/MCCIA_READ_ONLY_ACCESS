import django
from django.db import models

from adminapp.models import Country
from hallbookingapp.models import HallLocation
from membershipapp.models import UserDetail

# Create your models here.

IS_DELETED = (
    (True, True),
    (False, False),
)

PERSON_TITLE_OPTION = (

    ("Mr.", "Mr."),
    ("Mrs.", "Mrs."),
    ("Ms.", "Ms."),
)
PURPOSE_TO_VISIT = (

    ("WV", "Work Visit"),
    ("BU", "Business"),
)

VISA_TYPE = (
    ("Single", "Single Entry"),
    ("Multiple", "Multiple Entry"),
)

PASSPORT_COPY = (
    ('YES', 'YES'),
    ('NO', 'NO'),
)

DOC_PATH = 'PassportDocument'


class PlaceOfEmbassy(models.Model):
    country = models.ForeignKey(Country, blank=True, null=True)
    embassy_name = models.CharField(max_length=150, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.embassy_name)


RADIO_CHOICES = (
    ("Day", "Day"),
    ("Week", "Week"),
    ("Month", "Month"),
)


class Membership_Visa_Recommendations(models.Model):
    visa_recommendation_no = models.CharField(max_length=30, blank=True, null=True)
    to_which_country = models.ForeignKey(Country, blank=True, null=True)
    place_of_embassy = models.ForeignKey(PlaceOfEmbassy, blank=True, null=True)
    location = models.ForeignKey(HallLocation, blank=True, null=True)

    person_title = models.CharField(max_length=3,choices=PERSON_TITLE_OPTION,default="Mr.")
    person_name = models.CharField(max_length=80, blank=True, null=True)
    person_designation = models.CharField(max_length=70, blank=True)
    mobile_no = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=90, blank=True)
    purpose_to_visit = models.CharField(max_length=10,choices=PURPOSE_TO_VISIT,default="WV")
    visiting_from_date = models.DateField(default=django.utils.timezone.now,blank=True)
    visa_type = models.CharField(max_length=20, default='Single', blank=True, null=True, choices=VISA_TYPE)
    radio_choice = models.CharField(max_length=20, default='Day', blank=True, null=True, choices=RADIO_CHOICES)
    visitDurations = models.CharField(max_length=80, blank=True, null=True)
    total_visit_durations = models.CharField(max_length=80, blank=True, null=True)

    passport_no = models.CharField(max_length=30, blank=True, null=True)
    passport_valid_from_date = models.DateField(default=django.utils.timezone.now,blank=True)
    passport_valid_to_date = models.DateField(default=django.utils.timezone.now,blank=True)
    mcciamember = models.ForeignKey(UserDetail, blank=True, null=True)
    company_name = models.CharField(max_length=80, blank=True, null=True)
    address = models.TextField(blank=False, null=True)
    passport_copy = models.CharField(max_length=20, default='NO', blank=True, null=True, choices=PASSPORT_COPY)
    doc_file = models.FileField(upload_to='DOC_PATH',null=True, blank=True)
    created_by = models.CharField(max_length=80, blank=True, null=True)
    updated_by = models.CharField(max_length=80, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(choices=IS_DELETED, default=False)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.visa_recommendation_no)