from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'friends', views.friends, name='friends'),
    url(r'^getfeed/(?P<feedgroup>[\w\-]+)/(?P<userid>[\w\-]+)', views.getfeed, name='getfeed'),
    url(r'', views.index, name='index'),

]
