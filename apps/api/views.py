import json

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
import stream
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse

from .serializers import UserMiniProfileSerializer, SchoolSerializer, FeedModeratorSerializer, FollowSerializer, \
    GlobalGroupSerializer, FriendSerializer, UserMiniReadOnlyProfileSerializer, CourseSerializer
from .models import Page, UserMiniProfile, School, GlobalGroup, UserSectionMapping, Follow, FeedModerator, Course
from django.conf import settings

client = stream.connect(settings.STREAM_API_KEY, settings.STREAM_API_SECRET)


@login_required
def index(request):
    user = request.user
    user_token = client.create_user_token(user.username)
    print(user_token)
    context = {
        'user_token': user_token,
        'appId': settings.STREAM_APP_ID,
        'apiKey': settings.STREAM_API_KEY,
        'school' : request.user.mini_user_profile.school or '',
        'userid': request.user.username
    }
    if context['school']:
        context['schoolpage'] = request.user.mini_user_profile.school.page_id.pageid
    template = loader.get_template('frontend/index.html')
    print(context)
    return HttpResponse(template.render(context, request))

def followalltimelinestotheirusers():
    users = Page.objects.all()
    follows = []
    for page in users:
        pageobject = {
            'source': 'timeline:' + page.pageid,
            'target': 'user:' + page.pageid
        }
        follows.append(pageobject)
    client.follow_many(follows)


def createuserobjects():
    users = UserMiniProfile.objects.all()
    for user in users:
        client.users.update(
            user.user.username,
            {"name": user.first_name + ' ' + user.last_name,
             "profileImage": "http://www.gstatic.com/tv/thumb/persons/1083/1083_v9_ba.jpg"
             },
        )


@login_required
def friends(request):
    user = request.user
    userclass = UserMiniProfile.objects.get(user=user).user.section.section.section_class
    userfriends = Follow.objects.filter(from_page=user.mini_user_profile.page_id).values_list('to_page')
    friend_list = UserMiniProfile.objects.annotate(
        username=F('user__username'), schoolname=F('school__schoolname'),
        name=Concat(F('first_name'), Value(' '), F('last_name')),
        classname=F('user__section__section__section_class__class_level'),
        section=F('user__section__section__section_name')) \
        .values('pk', 'email', 'birthday', 'username', 'schoolname', 'classname', 'section', 'name', 'is_staff') \
        .filter(user__section__section__section_class=userclass, user__username__in=userfriends)
    non_friend_list = UserMiniProfile.objects.annotate(
        username=F('user__username'), schoolname=F('school__schoolname'),
        name=Concat(F('first_name'), Value(' '), F('last_name')),
        classname=F('user__section__section__section_class__class_level'),
        section=F('user__section__section__section_name')) \
        .values('pk', 'email', 'birthday', 'username', 'schoolname', 'classname', 'section', 'name', 'is_staff') \
        .filter(user__section__section__section_class=userclass).exclude(user__username__in=userfriends)

    friend_list_serializer = FriendSerializer(friend_list, many=True)
    non_friend_list_serializer = FriendSerializer(non_friend_list, many=True)
    return JsonResponse({"friends": friend_list_serializer.data, "non_friends": non_friend_list_serializer.data,
                         "userid": user.username}, safe=False)


@login_required
def search(request):
    school_name = request.GET.get('school')
    section = request.GET.get('section')
    class_level = request.GET.get('class')
    username = request.GET.get('user')
    user_friends = Follow.objects.filter(from_page=request.user.mini_user_profile.page_id).values_list('to_page')

    argument = {}
    if school_name:
        argument["user__mini_user_profile__school__schoolname__contains"] = school_name

    if section:
        argument["user__section__section__section_name"] = section

    if class_level:
        argument["user__section__section__section_class"] = class_level

    if username:
        argument["user__mini_user_profile__first_name__contains"] = username
        argument["user__mini_user_profile__last_name__contains"] = username
        argument["user__username__contains"] = username

    non_friend_list = UserMiniProfile.objects.annotate(
        username=F('user__username'), schoolname=F('school__schoolname'),
        name=Concat(F('first_name'), Value(' '), F('last_name')),
        classname=F('user__section__section__section_class__class_level'),
        section=F('user__section__section__section_name')) \
        .values('pk', 'email', 'birthday', 'username', 'schoolname', 'classname', 'section', 'name', 'is_staff') \
        .filter(**argument).exclude(user__username__in=user_friends)

    argument["user__username__in"] = user_friends

    friend_list = UserMiniProfile.objects.annotate(
        username=F('user__username'), schoolname=F('school__schoolname'),
        name=Concat(F('first_name'), Value(' '), F('last_name')),
        classname=F('user__section__section__section_class__class_level'),
        section=F('user__section__section__section_name')) \
        .values('pk', 'email', 'birthday', 'username', 'schoolname', 'classname', 'section', 'name', 'is_staff') \
        .filter(**argument)

    friend_list_serializer = FriendSerializer(friend_list, many=True)
    non_friend_list_serializer = FriendSerializer(non_friend_list, many=True)
    return JsonResponse({"friends": friend_list_serializer.data, "non_friends": non_friend_list_serializer.data,
                         "userid": request.user.username}, safe=False)


@login_required
def me(request):
    return JsonResponse(request.user.username, safe=False)


@login_required
def add_repost_reaction(request):
    if request.user.username != request.GET.get('username'):
        return HttpResponse("Y", status=500)
    activity_id = request.GET.get('id')
    to_user_username = request.GET.get('touser').replace("user:", "")
    client.reactions.add("repost", activity_id, user_id=request.user.username, target_feeds=["notification:" + to_user_username])

    user_feed = client.feed("user", request.user.username)
    user = UserMiniProfile.objects.filter(user__username=request.user.username)[0]
    to_user = UserMiniProfile.objects.filter(user__username=to_user_username)[0]
    activity_data = {
        'actor': user.first_name + ' ' + user.last_name,
        'actor_temp': {
            'data': {
                'name': user.first_name + ' ' + user.last_name,
                'id': user.user.username,
            }
        },
        'verb': 'repost',
        'object': request.GET.get('text'),
        'object_temp': {
            'verb': 'post',
            'actor': {
                'data': {
                    'name': to_user.first_name + ' ' + to_user.last_name
                }
            },
            'object': request.GET.get('text')
        },
    }
    user_feed.add_activity(activity_data)

    return HttpResponse("Y", status=200)

def getfeed(request, feedgroup, userid):
    print(request.POST)
    if request.method == 'GET':
        print("inside get")
        data = client.feed(feedgroup, userid).get(enrich=True, **request.GET)
        print(data)
        return JsonResponse(data)
    else:
        print("inside post")
        print(request.body)
        activity = json.loads(request.body.decode(encoding='UTF-8'))
        print(activity)
        return JsonResponse(client.feed(feedgroup, userid).add_activity(activity))

@login_required
def remove_comment(request):

    client.reactions.delete(request.GET.get('id'))
    return HttpResponse("N")

class GroupStats(APIView):
    def get(self, request):
        user_section = request.user.section.section
        user_follow_courses = Follow.objects.filter(from_page=request.user.mini_user_profile.page_id, type_of_page='course').values_list('to_page')
        courses_following = Course.objects.filter(course_section = user_section, page_id__in =user_follow_courses)
        courses_not_following = Course.objects.filter(course_section=user_section).exclude(page_id__in = user_follow_courses)
        courses_following_details = CourseSerializer(courses_following, many=True).data
        courses_not_following_details = CourseSerializer(courses_not_following, many=True).data
        user_follow_groups = Follow.objects.filter(from_page=request.user.mini_user_profile.page_id, type_of_page='globalgroup').values_list('to_page')
        global_group_following = GlobalGroup.objects.filter(page_id__in = user_follow_groups)
        global_group_not_following = GlobalGroup.objects.exclude(page_id__in=user_follow_groups)
        global_group_following_details = GlobalGroupSerializer(global_group_following, many=True).data
        global_group_not_following_details = GlobalGroupSerializer(global_group_not_following, many=True).data
        context = {
            'courses_following_details': courses_following_details,
            'courses_not_following_details' : courses_not_following_details,
            'global_group_following_details': global_group_following_details,
            'global_group_not_following_details': global_group_not_following_details
        }
        return Response(context, status=200)


class isModerator(APIView):
    def get_follow(self, from_page, to_page):
        followtable = Follow.objects.filter(from_page=from_page, to_page=to_page)
        return followtable

    def get(self, request, feedgroup):
        print(request.user)
        user_mini_profile = UserMiniReadOnlyProfileSerializer(request.user.mini_user_profile)

        try:
            group_object = GlobalGroup.objects.get(page_id=feedgroup)
            group_details = GlobalGroupSerializer(group_object).data
        except GlobalGroup.DoesNotExist:
            try:
                group_object = School.objects.get(page_id=feedgroup)
                group_details = SchoolSerializer(group_object).data
            except School.DoesNotExist:
                group_object = {}
                group_details = {}

        follow_relation = self.get_follow(request.user.mini_user_profile.page_id, feedgroup)
        print(follow_relation)
        following = False
        if follow_relation:
            following = True

        try:
            moderator = FeedModerator.objects.get(page=feedgroup, moderator=request.user)
            if moderator:
                return Response({'ismoderator': True, 'user_profile': user_mini_profile.data, 'group_details': group_details, 'following': following},
                                status=200)
            else:
                return Response({'ismoderator': False, 'user_profile': user_mini_profile.data, 'group_details': group_details, 'following': following},
                                status=200)
        except FeedModerator.DoesNotExist:
            return Response({'ismoderator': False, 'user_profile': user_mini_profile.data, 'group_details': group_details, 'following': following},
                            status=200)

class ApproveFeed(APIView):
    def post(self, request):
        feed_group = request.data['feed_group']
        feed_id = request.data['feed_id']
        approve = request.data['approve']
        decline = request.data['decline']
        print(request.user)
        try:
            moderator = FeedModerator.objects.get(page=feed_group, moderator=request.user)
            print(moderator)
            if moderator:
                if approve == True:
                    activity = client.get_activities(ids=[feed_id])['results'][0]
                    group_feed = client.feed('globalgroup', feed_group)
                    group_feed.add_activity(activity)
                    unapproved_group_feed = client.feed('unapprovedgroup', feed_group)
                    unapproved_group_feed.remove_activity(feed_id)
                    return Response({'success': True},
                                    status=200)
                elif decline == True:
                    unapproved_group_feed = client.feed('unapprovedgroup', feed_group)
                    unapproved_group_feed.remove_activity(feed_id)
                    return Response({'success': True},
                                    status=200)
            else:
                return Response({'ismoderator': False},
                                status=200)
        except FeedModerator.DoesNotExist:
            return Response({'ismoderator': False},
                            status=200)


class FollowApi(APIView):
    def get_follow(self, from_page, to_page):
        followtable = Follow.objects.filter(from_page=from_page, to_page=to_page)
        return followtable

    def post(self, request):
        print(request.data)
        follow_relation = self.get_follow(request.data['from_page'], request.data['to_page'])
        print(follow_relation)
        if follow_relation:
            follow_relation.delete()
            from_page = client.feed('timeline', request.data['from_page'])
            from_page.unfollow(request.data['type_of_page'], request.data['to_page'])
            return Response({'status': 'delete successful'},
                            status=200)
        else:
            new_follow_serializer = FollowSerializer(data=request.data)
            if new_follow_serializer.is_valid():
                new_follow_serializer.save()
                from_page = client.feed('timeline', request.data['from_page'])
                from_page.follow(request.data['type_of_page'], request.data['to_page'])
                return Response(new_follow_serializer.data,
                                status=200)
            return Response(new_follow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherProfile(APIView):

    def get_school_teachers(self, school):
        try:
            user_mini_profile = UserMiniProfile.objects.filter(school=school, is_staff=True)
            print(user_mini_profile)
            return user_mini_profile
        except UserMiniProfile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        print(pk)
        user_mini_profile = self.get_school_teachers(pk)
        user_mini_serializer = UserMiniProfileSerializer(user_mini_profile, many=True)
        return Response(user_mini_serializer.data)

    def get_object(self, pk):
        try:
            return UserMiniProfile.objects.get(pk=pk)
        except UserMiniProfile.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        teacher = self.get_teacher(pk)
        serializer = UserMiniProfileSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFeedModerator(APIView):

    def post(self, request):
        feedmoderatorserializer = FeedModeratorSerializer(data=request.data)

        if feedmoderatorserializer.is_valid():
            feedmoderatorserializer.save()
            return Response(feedmoderatorserializer.data)
        page = Page.objects.get(pageid=request.data.page)
        follows = []
        pageobject = {
            'source': 'user:' + request.data.moderator,
            'target': page.ownertype + request.data.page
        }
        follows.append(pageobject)
        client.follow_many(follows)
        return Response(feedmoderatorserializer.errors, status=status.HTTP_400_BAD_REQUEST)

