# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-31 07:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_level', models.CharField(max_length=5)),
                ('display_name', models.CharField(max_length=10)),
                ('num_sections', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=150)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=144, null=True)),
                ('year', models.IntegerField(default=2020)),
                ('courseno', models.CharField(max_length=50)),
                ('courserun', models.CharField(max_length=30)),
                ('course_id', models.CharField(max_length=80)),
                ('course_status', models.CharField(max_length=3)),
                ('course_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Class')),
            ],
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_type', models.CharField(max_length=30)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=50)),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Feed')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Feed')),
                ('from_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('short_name', models.CharField(db_index=True, help_text=b'Please do not use spaces or special characters. Only allowed special characters are period (.), hyphen (-) and underscore (_).', max_length=255, verbose_name=b'Short Name')),
                ('description', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, help_text=b'Please add only .PNG files for logo images. This logo will be used on certificates.', max_length=255, null=True, upload_to=b'organization_logos')),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('pageid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('ownertype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolname', models.CharField(blank=True, max_length=50, null=True)),
                ('principal', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=50, null=True)),
                ('board', models.CharField(blank=True, max_length=20, null=True)),
                ('schoollogo', models.ImageField(blank=True, default=b'school_logo/no-image.jpg', upload_to=b'school_logo')),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school_profile', to='api.Organization')),
                ('page_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school', to='api.Page')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=5)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('section_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Class')),
            ],
        ),
        migrations.CreateModel(
            name='UserMiniProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=40, null=True)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('email', models.CharField(blank=True, max_length=40, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=40, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('is_staff', models.BooleanField()),
                ('page_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='api.Page')),
                ('school', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.School')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserOrganizationMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_amc_admin', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSectionMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Section')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='organization',
            name='users',
            field=models.ManyToManyField(related_name='organizations', through='api.UserOrganizationMapping', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='group',
            name='page_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='api.Page'),
        ),
        migrations.AddField(
            model_name='follows',
            name='from_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_follow', to='api.Page'),
        ),
        migrations.AddField(
            model_name='follows',
            name='to_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_follow', to='api.Page'),
        ),
        migrations.AddField(
            model_name='feed',
            name='from_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_page', to='api.Page'),
        ),
        migrations.AddField(
            model_name='feed',
            name='to_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_page', to='api.Page'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Section'),
        ),
        migrations.AddField(
            model_name='course',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Organization'),
        ),
        migrations.AddField(
            model_name='course',
            name='page_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='api.Page'),
        ),
        migrations.AddField(
            model_name='comments',
            name='feed_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Feed'),
        ),
        migrations.AddField(
            model_name='comments',
            name='page_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Page'),
        ),
        migrations.AddField(
            model_name='class',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Organization'),
        ),
    ]