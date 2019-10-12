import django
from django.db import models
from django.contrib.auth.models import User


IS_DELETED = (
    (True, True),
    (False, False),
)

ROLE_STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
)

class UserPrivilege(models.Model):
    privilege = models.CharField(max_length=500, blank=False, null=False)
    #parent = models.ForeignKey('self', blank=True, null=True)
    module_name = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.privilege)


class UserRole(models.Model):
    role = models.CharField(max_length=500, blank=False, null=False)
    description = models.CharField(max_length=500, blank=True, null=True)
    privilege = models.ManyToManyField(UserPrivilege)
    status = models.CharField(max_length=20, default='Active', choices=ROLE_STATUS)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    is_active = models.BooleanField(choices=IS_DELETED, default=True)

    def __unicode__(self):
        return unicode(self.role)


class Department(models.Model):
    department_name = models.CharField(max_length=250, blank=False, null=False)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.department_name)   


class Designation(models.Model):
    designation_name = models.CharField(max_length=250, blank=False, null=False)
    created_by = models.CharField(max_length=50, blank=False, null=False)
    created_on = models.DateTimeField(default=django.utils.timezone.now)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)

    def __unicode__(self):
        return unicode(self.designation_name)                


class SystemUserProfile(User):

    USER_STATUS = (
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
    )

    USER_TYPE = (
        ('SUPER_ADMIN', 'SUPER_ADMIN'),
        ('WEB_USER', 'WEB_USER'),
        ('MEMBER', 'MEMBER'),
        ('EVENT', 'EVENT'),
        ('ADMIN', 'ADMIN'),
    )
    name = models.CharField(max_length=200, blank=True, null=True)
    department = models.ForeignKey(Department, blank=True, null=True)
    designation = models.ForeignKey(Designation, blank=True, null=True)
    contact_no = models.CharField(max_length=50, blank=False, null=False)
    type = models.CharField(max_length=20, default='WEB_USER', choices=USER_TYPE)    
    role = models.ForeignKey(UserRole, blank=True, null=True)
    user_status = models.CharField(max_length=20, default='ACTIVE', choices=USER_STATUS)
    user_type = models.CharField(max_length=20, blank=True, null=True, choices=USER_TYPE)
    is_deleted = models.BooleanField(choices=IS_DELETED, default=False)
    # is_active = models.BooleanField(choices=IS_DELETED, default=True)
    created_by = models.CharField(max_length=500, blank=False, null=False)

    created_on = models.DateTimeField(default=django.utils.timezone.now)
    updated_date = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=500, blank=True, null=True)

    def __unicode__(self):
        return unicode(str(self.first_name) + ' ' + str(self.last_name))
