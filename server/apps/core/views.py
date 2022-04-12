from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Submission,Vote
from django.views import View
from .forms import SubmissionForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.

class voteView(View):

    def unvote(self, vote):
        if len(vote) != 0:
            vote.delete()

    def vote(self, v, submission, user):
        if len(v) == 0:
            v = Vote(voter=user, submission=submission)
            v.save()

    def get(self,request,id, *args, **kwargs):
        user = request.user
        isVote = 'unvote' not in request.path
        print(isVote)
        submission = Submission.objects.get(id=id)
        votes = Vote.objects.filter(submission=submission)
        v = votes.filter(voter=user)
        if isVote:
            self.vote(v,submission,user)
        else:
            self.unvote(v)
        return redirect('/')



class HomeView(View):

    def get_votes(self, user, submission):
        if user.is_authenticated:
            v = Vote.objects.filter(submission=submission)
            return v.filter(voter=user)
        return []

    def get(self,request, *args, **kwargs):
        user = request.user
        submissions = list(Submission.objects.all())
        votes = []
        for submission in submissions:
            v = self.get_votes(user, submission)
            if len(v) != 0:
                votes.append(submission.id)

            submission.count_votes()

        context = {
            'submissions': submissions,
            'votes': votes
        }
        response = render(request, 'core/main.html', context=context)  # render the html with the context
        return HttpResponse(response)

    #def post(self,request,*args,**kwargs):


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


