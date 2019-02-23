from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
import datetime
import stream

from .models import Page
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
            'source': 'page:' + page.pageid,
            'target': 'timeline:' + page.pageid
        }
        follows.append(pageobject)
    client.follow_many(follows)


def getusertoken(request):
    pass

