from django.conf.urls import url

from .views import Follow
from . import views

urlpatterns = [
    url(r'api/friends', views.friends, name='friends'),
    url(r'api/me', views.me, name='me'),
    url(r'^getfeed/(?P<feedgroup>[\w\-]+)/(?P<userid>[\w\-]+)', views.getfeed, name='getfeed'),
    url(r'^api/follow', Follow.as_view()),
    url(r'', views.index, name='index'),


]
