from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.contrib.auth.models import User
import stream
from django.conf import settings

from .models import Course, Page, School, UserMiniProfile

client = stream.connect(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)


@receiver(post_save, sender = UserMiniProfile)
def new_stream_user(sender, instance, **kwargs):
    user_page = Page(pageid=instance.user.username, ownertype='user')
    user_page.save()
    instance.page_id = user_page
    instance.save()
    client.users.add(
        instance.user.username,
        {"name": instance.first_name + ' ' + instance.last_name
         },
    )
    follows = []
    pageobject = {
        'source': 'timeline:' + instance.user.username,
        'target': 'user:' + instance.user.username,
    }
    follows.append(pageobject)
    pageobject = {
        'source': 'timeline:' + instance.user.username,
        'target': 'user:' + instance.school.page_id,
    }
    follows.append(pageobject)
    client.follow_many(follows)


@receiver(post_save, sender = Course)
def new_stream_course(sender, instance, **kwargs):
    course_page = Page(pageid=instance.course_id, ownertype='course')
    course_page.save()
    if instance.page_id != course_page:
        instance.page_id = course_page
        instance.save(update_fields=['page_id'])


@receiver(post_save, sender = School)
def new_stream_school(sender, instance, **kwargs):
    print(instance, instance.schoolname)
    school_page, created = Page.objects.get_or_create(pageid=instance.organization.name, ownertype='school')
    if instance.page_id != school_page:
        instance.page_id = school_page
        instance.save(update_fields=['page_id'])


