import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
import datetime
import stream
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserMiniProfileSerializer, SchoolSerializer, FeedModeratorSerializer, FollowSerializer, \
    GlobalGroupSerializer
from .models import Page, UserMiniProfile, School, GlobalGroup
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
        'apiKey': settings.STREAM_API_KEY
    }
    template = loader.get_template('frontend/index.html')
    return HttpResponse(template.render(context, request))

def followalluserstotheirtimeline():
    users = Page.objects.all()
    follows = []
    for page in users:
        pageobject = {
            'source': 'user:' + page.pageid,
            'target': 'timeline:' + page.pageid
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
    userclass = UserMiniProfile.objects.get(user = user).user.section.section.section_class
    friends = UserMiniProfile.objects.filter(user__section__section__section_class=userclass)

    context = {
        'friends': friends,
    }
    template = loader.get_template('frontend/friends.html')
    return HttpResponse(template.render(context, request))

def groups(request):
    availablegroups = GlobalGroup.objects.all()
    groupserializer = GlobalGroupSerializer(availablegroups)
    return Response(groupserializer.data,
                    status=200)


def getfeed(request,feedgroup, userid):
    print(request.POST)
    if request.method == 'GET':
        print("inside get")
        return JsonResponse(client.feed(feedgroup, userid).get(**request.GET))
    else:
        print("insdie post")
        print(request.body)
        activity = json.loads(request.body.decode(encoding='UTF-8'))
        return JsonResponse(client.feed(feedgroup, userid).add_activity(activity))




class AddNewGlobalGroup(APIView):
    def post(selfr, request):
        newglobalgroup = GlobalGroupSerializer(request.data)
        if newglobalgroup.is_valid:
            newglobalgroup.save()
            return Response(newglobalgroup.data,
                            status=200)
        return Response(newglobalgroup.errors, status=status.HTTP_400_BAD_REQUEST)




class ClassStudentList(APIView):
    def get_users_of_class(class_id):
        users = UserMiniProfile.objects.filter(section__section__section_class=class_id)
        return users
    def get(self, request, class_id):
        users = self.get_users_of_class(class_id)
        userprofiles = UserMiniProfileSerializer(users)
        return Response(userprofiles.data,
                        status=200)


class Follow(APIView):
    def post(self, request):
        new_follow_serializer = FollowSerializer(request.data)
        if new_follow_serializer.is_valid():
            new_follow_serializer.save()
            from_page = client.feed('timeline', request.data.from_page)
            from_page.follow(request.data.type_of_page, request.data.to_page)
            return Response(new_follow_serializer.data,
                            status=200)
        return Response(new_follow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TeacherProfile(APIView):
    #authentication_classes = (OAuth2AuthenticationAllowInactiveUser,JwtAuthentication)
    #permission_classes = (IsAuthenticated,)

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


class StartSchoolFeed(APIView):
    def get(self, request, pk):
        follows= []
        schoolobject = School.objects.get(id=pk)
        schoolobject.school_feed = True
        schoolobject.save()
        schoolobjectserializer = SchoolSerializer()
        return Response(schoolobjectserializer.data)

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


class AddNewGlobalGroup(APIView):
    def post(self, request):
        pass

class AddNewSchoolGroup(APIView):
    def post(self, request):
        pass

class AddNewCourseGroup(APIView):
    def post(self, request):
        pass






