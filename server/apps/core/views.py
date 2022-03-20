from django.shortcuts import render
from django.http import HttpResponse
from ..accounts.models import User
import datetime

# Create your views here.


def news(request):
    # fetch date and time

    # if you have empty the db and need  to create one
    # user = User(username='Bagansio')
    # user.save()


    user = User.objects.get(pk=1) #Bagansio ^^


    now = datetime.datetime.now()
    # convert to string
    html = "Time is {} ".format(now)
    html += str(user.id) + " " + user.username
    # return response
    return HttpResponse(html)
