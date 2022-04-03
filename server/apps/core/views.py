from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Submission
from django.views import View
from .forms import SubmissionForm
import datetime

# Create your views here.

def news(request):
    # fetch date and time

    # if you have empty the db and need  to create one
    #user = User(username='Bagansio')
    #user.save()


    user = request.user
    submissions = list(Submission.objects.all())
    #submissions = Submission.objects.get()
    now = datetime.datetime.now()
    context = {
        'submissions': submissions,
    }
    response = render(request, 'core/main.html', context=context)  # render the html with the context
    return HttpResponse(response)


class SubmissionsView(View):


    def get(self,request, *args, **kwargs):

        context = {
            'submit_form': SubmissionForm(),
        }
        response = render(request, 'core/submit.html', context=context)  # render the html with the context
        return HttpResponse(response)


    def post(self,request,*args,**kwargs):

        user = request.user

        submission_form = SubmissionForm(request.POST)
        status = 404
        if submission_form.is_valid():
            submission_form.savedb(user)
            status = 200
        return redirect('news')


