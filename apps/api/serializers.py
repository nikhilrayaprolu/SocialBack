from django.contrib.auth.models import User
from rest_framework import serializers

from apps.api.models import Organization, School, Class, Section, Course, UserMiniProfile, UserSectionMapping


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'short_name', 'edx_uuid')

class SchoolSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(queryset=Organization.objects.all(), slug_field='name')
    class Meta:
        model = School
        fields = ('id','organization', 'schoolname', 'principal', 'email', 'contact_number', 'address', 'website', 'board')

class ClassSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Class
        fields = ('id','organization','class_level', 'display_name', 'num_sections')

class SectionSerializer(serializers.ModelSerializer):
    section_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())

    class Meta:
        model = Section
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    course_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    course_section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = Course
        fields = '__all__'

class UserMiniProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserMiniProfile
        fields = '__all__'

class UserSectionMappingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = UserSectionMapping
        fields = '__all__'
