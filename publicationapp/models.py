import django
from django.db import models
from backofficeapp.models import SystemUserProfile

# Create your models here.
FILE_PATH = 'Publication/Publication_File'
COVER_PATH = 'Publication/CoverImages'

PUBLICATION_TYPE = (
    (0, 'Sampada'),
    (1, 'Annual Report'),
    (2, 'World of Business'),
)

IS_DELETED = (
    (True, True),
    (False, False),
)


class PublicationFile(models.Model):
    publication_type = models.IntegerField(choices=PUBLICATION_TYPE, default=0)
    file_path = models.ImageField(upload_to=FILE_PATH, null=True, blank=True)
    cover_path = models.ImageField(upload_to=COVER_PATH, null=True, blank=True)  # Upload only for Sampda and Annual Report
    publish_date = models.DateField(blank=True, null=True)
    contact_person = models.ForeignKey(SystemUserProfile, blank=True, null=True)
    volume_no = models.CharField(max_length=20, blank=True, null=True)
    issue_no = models.CharField(max_length=20, blank=True, null=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(str(self.id) + '_' + str(self.get_publication_type_display()) + '_' + str(self.publish_date))