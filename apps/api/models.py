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
                  'are period (.), hyphen (-) and underscore (_).',
        primary_key=True
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

    def natural_key(self):
        return (self.short_name,)

    def __str__(self):
        return self.short_name


class UserOrganizationMapping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_amc_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.organization + ' ' + self.user


class Page(models.Model):
    pageid = models.CharField(max_length=20, primary_key=True)
    ownertype = models.CharField(max_length=50)

    def __str__(self):
        return self.pageid


class School(models.Model):
    organization = models.OneToOneField(Organization, related_name='school_profile', on_delete=models.CASCADE,
                                        primary_key=True)
    schoolname = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    principal = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=50, blank=True, null=True)
    board = models.CharField(max_length=20, blank=True, null=True)
    schoollogo = models.ImageField(blank=True, upload_to='school_logo', default='school_logo/no-image.jpg')
    page_id = models.ForeignKey(Page, null=True, blank=True, related_name="school", on_delete=models.CASCADE)
    school_feed = models.BooleanField(default=False)

    def __str__(self):
        return self.schoolname


class Class(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    class_level = models.CharField(max_length=5)
    display_name = models.CharField(max_length=10)
    num_sections = models.IntegerField(default=0)

    def __str__(self):
        return self.class_level


class Section(models.Model):
    section_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section_name = models.CharField(max_length=5)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.section_name + ' ' + self.section_class.display_name


class Course(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    course_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    course_section = models.ForeignKey(Section, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=50)
    description = models.CharField(max_length=144, blank=True, null=True)
    year = models.IntegerField(default=2020)
    courseno = models.CharField(max_length=50)
    courserun = models.CharField(max_length=30)
    course_id = models.CharField(max_length=80, primary_key=True)
    course_status = models.CharField(max_length=3)
    page_id = models.ForeignKey(Page, null=True, blank=True, related_name="course", on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name


class UserMiniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mini_user_profile', primary_key=True)
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    contact_number = models.CharField(max_length=40, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(blank=True)
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.CASCADE)
    page_id = models.OneToOneField(Page, null=True, blank=True, related_name="user", on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class UserSectionMapping(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='section')
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' ' + self.section.section_name


class FeedModerator(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='moderators')
    moderator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_moderated')


class GlobalGroup(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    longname = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=400, blank=True, null=True)
    group_image = models.ImageField(blank=True, upload_to='school_logo', default='school_logo/no-image.jpg')
    page_id = models.OneToOneField(Page, related_name="globalgroup", primary_key=True)


class SchoolGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    page_id = models.OneToOneField(Page, related_name="schoolgroup", on_delete=models.CASCADE, primary_key=True)
    school = models.ForeignKey(School, blank=True, null=True, on_delete=models.CASCADE, related_name='school_groups')
    globalgroup = models.ForeignKey(GlobalGroup, null=True, blank=True, related_name="schoolgroups")

class Follow(models.Model):
    from_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='from_follow')
    to_page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='to_follow')
    type_of_page = models.CharField(max_length=20)
