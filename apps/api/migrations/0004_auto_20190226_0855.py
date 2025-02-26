# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-26 08:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_auto_20190202_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='FeedModerator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moderator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_moderated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalGroup',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=400)),
                ('page_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='globalgroup', serialize=False, to='api.Page')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolGroup',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=400)),
                ('page_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='schoolgroup', serialize=False, to='api.Page')),
                ('globalgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schoolgroups', to='api.GlobalGroup')),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='feed_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='page_id',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='from_page',
        ),
        migrations.RemoveField(
            model_name='feed',
            name='to_page',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='from_page',
        ),
        migrations.RemoveField(
            model_name='follow',
            name='to_page',
        ),
        migrations.RemoveField(
            model_name='group',
            name='page_id',
        ),
        migrations.RemoveField(
            model_name='hashtag',
            name='feed',
        ),
        migrations.RemoveField(
            model_name='like',
            name='feed',
        ),
        migrations.RemoveField(
            model_name='like',
            name='from_page',
        ),
        migrations.RemoveField(
            model_name='course',
            name='id',
        ),
        migrations.RemoveField(
            model_name='organization',
            name='id',
        ),
        migrations.RemoveField(
            model_name='school',
            name='id',
        ),
        migrations.RemoveField(
            model_name='userminiprofile',
            name='id',
        ),
        migrations.AddField(
            model_name='school',
            name='school_feed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.CharField(max_length=80, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='organization',
            name='short_name',
            field=models.CharField(db_index=True, help_text=b'Please do not use spaces or special characters. Only allowed special characters are period (.), hyphen (-) and underscore (_).', max_length=255, primary_key=True, serialize=False, verbose_name=b'Short Name'),
        ),
        migrations.AlterField(
            model_name='school',
            name='organization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='school_profile', serialize=False, to='api.Organization'),
        ),
        migrations.AlterField(
            model_name='userminiprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='usersectionmapping',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Feed',
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='HashTag',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
        migrations.AddField(
            model_name='schoolgroup',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_groups', to='api.School'),
        ),
        migrations.AddField(
            model_name='feedmoderator',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderators', to='api.Page'),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='course_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_group', to='api.Course'),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='page_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coursegroup', to='api.Page'),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school_course_groups', to='api.School'),
        ),
    ]
