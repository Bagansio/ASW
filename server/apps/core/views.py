from django.shortcuts import render, redirect
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
    #user = User(username='Bagansio')
    #user.save()


    user = User.objects.get(pk=1) #Bagansio ^^
    submissions = list(Submission.objects.all())
    #submissions = Submission.objects.get()
    now = datetime.datetime.now()
    context = {
        'submissions': submissions,
        'user': user,
    }
    response = render(request, 'core/main.html', context=context)  # render the html with the context
    return HttpResponse(response)


class SubmissionsView(View):

    user = User.objects.get(pk=1)  # Bagansio ^^

    def get(self,request, *args, **kwargs):

        now = datetime.datetime.now()
        #to create testing submissions
        #submission = Submission(title="Yepa    ", url="https://stackoverflow.com/", text="Yepa", created_at=now, author=user)
        #submission.save()

        context = {
            'submit_form': SubmissionForm(),
            'user': self.user
        }
        response = render(request, 'core/submit.html', context=context)  # render the html with the context
        return HttpResponse(response)


    def post(self,request,*args,**kwargs):
        submission_form = SubmissionForm(request.POST)
        status = 404
        if submission_form.is_valid():
            submission_form.savedb(self.user)
            status = 200
        return redirect('news')


