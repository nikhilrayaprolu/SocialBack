from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Organization, School, Class, Section, Course, UserMiniProfile, UserSectionMapping, Page, \
    FeedModerator, GlobalGroup, Follow


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'short_name', 'edx_uuid')

class FeedModeratorSerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    moderator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = FeedModerator
        fields = '__all__'


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
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())

    class Meta:
        model = UserMiniProfile
        fields = '__all__'

class UserMiniReadOnlyProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    school = serializers.SlugRelatedField(read_only=True,
                                          source='school.page_id',
        slug_field='pageid')

    class Meta:
        model = UserMiniProfile
        fields = '__all__'


class UserSectionMappingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = UserSectionMapping
        fields = '__all__'

class GlobalGroupSerializer(serializers.ModelSerializer):
    page_id = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    class Meta:
        model = GlobalGroup
        fields = '__all__'


class SchoolGroupSerializer(serializers.ModelSerializer):
    page_id = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    globalgroup = serializers.PrimaryKeyRelatedField(queryset=GlobalGroup.objects.all())
    class Meta:
        model = School
        fields = '__all__'


class CourseGroupSerializer(serializers.ModelSerializer):
    page_id = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    cousre_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Course
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    from_page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    to_page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    class Meta:
        model = Follow
        fields = '__all__'

class FriendSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    email = serializers.EmailField()
    birthday = serializers.DateField()
    username = serializers.CharField()
    schoolname = serializers.CharField()
    classname = serializers.CharField()
    section = serializers.CharField()
    name = serializers.CharField()
    is_staff = serializers.BooleanField()





