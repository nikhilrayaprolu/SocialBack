from django.conf.urls import url

from .views import FollowApi, isModerator, ApproveFeed, GroupStats
from . import views

urlpatterns = [
    url(r'api/friends', views.friends, name='friends'),
    url(r'api/me', views.me),
    url(r'api/groupstats', GroupStats.as_view()),
    url(r'api/add_reaction', views.add_repost_reaction),
    url(r'api/delete_reaction', views.remove_comment, name='remove_comment'),
    url(r'api/search/user', views.search, name='search'),
    url(r'^getfeed/(?P<feedgroup>[\w\-]+)/(?P<userid>[\w\-]+)', views.getfeed, name='getfeed'),
    url(r'^api/follow', FollowApi.as_view()),
    url(r'^api/moderator/(?P<feedgroup>[\w\-]+)', isModerator.as_view()),
    url(r'^api/approve/', ApproveFeed.as_view()),
    url(r'', views.index, name='index'),

]
