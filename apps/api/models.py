from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from jsonfield.fields import JSONField
# Create your models here.


class Organization(models.Model):
    """
    An Organization is a representation of an entity which publishes/provides
    one or more courses delivered by the LMS. Organizations have a base set of
    metadata describing the organization, including id, name, and description.
    """
    name = models.CharField(max_length=255, db_index=True)
    short_name = models.CharField(
        max_length=255, db_index=True, verbose_name='Short Name',
        help_text='Please do not use spaces or special characters. Only allowed special characters '
                    'are period (.), hyphen (-) and underscore (_).'
    )
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(
        upload_to='organization_logos',
        help_text='Please add only .PNG files for logo images. This logo will be used on certificates.',
        null=True, blank=True, max_length=255
    )
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(
        User,
        through='UserOrganizationMapping',
        related_name="organizations"
    )

class UserOrganizationMapping(models.Model):
    user = models.ForeignKey(User)
    organization = models.ForeignKey(Organization)
    is_active = models.BooleanField(default=True)
    is_amc_admin = models.BooleanField(default=False)



class Page(models.Model):
    pageid = models.CharField(max_length=20, primary_key=True)
    ownertype = models.CharField(max_length=50)


class School(models.Model):
    organization = models.OneToOneField(Organization, related_name='school_profile')
    schoolname = models.CharField(max_length=50, blank=True, null=True)
    principal = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    board = models.CharField(max_length=20, blank=True, null=True)
    schoollogo = models.ImageField(blank=True, upload_to='school_logo', default='school_logo/no-image.jpg')
    page_id = models.ForeignKey(Page, null=True, blank=True, related_name="school")


class Class(models.Model):
    organization = models.ForeignKey(Organization)
    class_level = models.CharField(max_length=5)
    display_name = models.CharField(max_length=10)
    num_sections = models.IntegerField(default=0)


class Section(models.Model):
    section_class = models.ForeignKey(Class)
    section_name = models.CharField(max_length=5)
    description = models.CharField(max_length=200, blank=True, null=True)


class Course(models.Model):
    organization = models.ForeignKey(Organization)
    course_class = models.ForeignKey(Class)
    course_section = models.ForeignKey(Section)
    course_name = models.CharField(max_length=50)
    description = models.CharField(max_length=144, blank=True, null=True)
    year = models.IntegerField(default=2020)
    courseno = models.CharField(max_length=50)
    courserun = models.CharField(max_length=30)
    course_id = models.CharField(max_length=80)
    course_status = models.CharField(max_length=3)
    page_id = models.ForeignKey(Page, null=True, blank=True, related_name="course")



class UserMiniProfile(models.Model):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    contact_number = models.CharField(max_length=40, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(blank=True)
    school = models.ForeignKey(School, blank=True, null=True)
    page_id = models.ForeignKey(Page, null=True, blank=True, related_name="user")


class UserSectionMapping(models.Model):
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section)

class Group(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    page_id = models.ForeignKey(Page, null=True, blank=True, related_name="group")

class Follow(models.Model):
    from_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='from_follow')
    to_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='to_follow')


class Feed(models.Model):
    from_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='from_page')
    to_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='to_page')
    feed_type = models.CharField(max_length=30)
    created_time = models.DateTimeField(default=timezone.now)
    updated_time = models.DateTimeField(default=timezone.now)
    body = JSONField  # Supposed to be JSON Field


class Like(models.Model):
    from_page = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)


class HashTag(models.Model):
    hashtag = models.CharField(max_length=50)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)


class Comment(models.Model):
    comment = models.CharField(max_length=150)
    time = models.DateTimeField(default=timezone.now)
    feed_id = models.ForeignKey(Feed, on_delete=models.CASCADE)
    page_id = models.ForeignKey(Page, null=True, blank=True)
