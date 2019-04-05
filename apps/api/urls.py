from django.conf.urls import url

from . import views as social_back

urlpatterns = [
    url(r'friendslist', social_back.friends, name='friends'),
    url(r'groupstats', social_back.GroupStats.as_view()),
    url(r'me', social_back.me, name='me'),
    url(r'search/user', social_back.search, name='search'),
    url(r'^getfeed/(?P<feedgroup>[\w\-]+)/(?P<userid>[\w\-]+)', social_back.getfeed, name='getfeed'),
    url(r'^follow', social_back.FollowApi.as_view()),
    url(r'^moderator/(?P<feedgroup>[\w\-]+)', social_back.isModerator.as_view()),
    url(r'^approve/', social_back.ApproveFeed.as_view()),
    url(r'', social_back.index, name='index'),


]
