from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from ..accounts.models import User
from .models import Submission
from django.views import View
from .forms import SubmissionForm
import datetime

# Create your views here.


def news(request):
    # fetch date and time

    # if you have empty the db and need  to create one
    # user = User(username='Bagansio')
    # user.save()


    user = User.objects.get(pk=1) #Bagansio ^^
    submissions = Submission.objects.all()
    #submissions = Submission.objects.get()
    now = datetime.datetime.now()
    # convert to string
    html = "Time is {} ".format(now)
    html += str(user.id) + " " + user.username
    # return response
    tmp = loader.get_template('core/main.html')  # load the html
    document = tmp.render() #render the html with the context
    return HttpResponse(document)

class SubmissionsView(View):


    def get(self,request, *args, **kwargs):
        user = User.objects.get(pk=1)  # Bagansio ^^
        context = {
            'submit_form': SubmissionForm(),
            'user': user
        }
        response = render(request, 'core/submit.html', context=context)  # render the html with the context
        return HttpResponse(response)






