import django
from django.db import models
from membershipapp.models import UserDetail
from adminapp.models import Committee
from backofficeapp.models import SystemUserProfile


# Create your models here.
IS_DELETED = (
    (True, True),
    (False, False),
)



EVENT_PRIORITY = (
    (0, 'No Priority'),
    (1, 'Priority 1'),
    (2, 'Priority 2'),
    (3, 'Priority 3'),
)

FILE_PATH ='printmedia/'


class MCCIABanner(models.Model):
    document_files = models.FileField(upload_to=FILE_PATH, max_length=500, null=True, blank=True)
    banner_link = models.TextField(blank=False, null=True)
    is_expired = models.BooleanField(choices=IS_DELETED, default=False)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    expire_date = models.DateTimeField(null=True, blank=True)
    creation_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.id)

class MCCIALinkToShare(models.Model):
    document_files = models.FileField(upload_to=FILE_PATH, max_length=500, null=True, blank=True)
    link_to_share = models.TextField(blank=False, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    creation_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.id)        

class MCCIALEADERSHIP(models.Model):
    leader_designation = models.CharField(max_length=200, blank=False, null=True)
    leader_name = models.CharField(max_length=200, blank=False, null=True)
    leader_post = models.CharField(max_length=200, blank=False, null=True)
    leader_organisation = models.CharField(max_length=200, blank=False, null=True)
    
    created_by = models.CharField(max_length=80, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    def __unicode__(self):
        return unicode(self.id)

class MCCIATeam(models.Model):
    member_designation = models.CharField(max_length=200, blank=False, null=True)
    member_name = models.CharField(max_length=200, blank=False, null=True)
    member_post = models.CharField(max_length=200, blank=False, null=True)    
    
    created_by = models.CharField(max_length=80, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    def __unicode__(self):
        return unicode(self.id)

class MCCIATeamImage(models.Model):
    leader_id = models.ForeignKey(MCCIALEADERSHIP, blank=True, null=True)
    document_files = models.FileField(upload_to=FILE_PATH, max_length=500, null=True, blank=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    creation_date = models.DateTimeField(null=True, blank=True)
    created_by = models.CharField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.id)

class MCCIAVideoLinks(models.Model):
    video_link = models.CharField(max_length=200, blank=False, null=True)
    video_type = models.CharField(max_length=200, blank=False, null=True)
    
    created_by = models.CharField(max_length=80, blank=False, null=True)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    def __unicode__(self):
        return unicode(self.id)        

