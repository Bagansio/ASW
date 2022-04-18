from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission, Vote
from django.views import View
from .forms import SubmissionForm
from django.contrib.auth.models import User



# util functions

def get_votes(user, submission):
    if user.is_authenticated:
        v = Vote.objects.filter(submission=submission)
        return v.filter(voter=user)
    return []


def load_submission(user, submissions):
    votes = []

    for submission in submissions:
        v = get_votes(user, submission)
        if len(v) != 0:
            votes.append(submission.id)
        submission.count_comments()
        submission.count_votes()

    return votes


# main/home view


class HomeView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        submissions = list(Submission.objects.all())
        votes = load_submission(user, submissions)

        context = {
            'submissions': submissions,
            'votes': votes
        }
        response = render(request, 'core/home.html', context=context)  # render the html with the context
        return HttpResponse(response)

    # def post(self,request,*args,**kwargs):


# submitted/username view


class SubmittedView(View):

    def get(self, request, username):
        user = request.user

        try:
            user_searched = User.objects.get(username=username)

        except Exception as e:
            return HttpResponse('No such user.')

        submissions = list(Submission.objects.filter(author=user_searched))

        votes = load_submission(user, submissions)

        context = {
            'submissions': submissions,
            'votes': votes
        }
        response = render(request, 'core/home.html', context=context)  # render the html with the context
        return HttpResponse(response)


# vote/unvote view


class voteView(View):

    def unvote(self, vote):
        if len(vote) != 0:
            vote.delete()

    def vote(self, v, submission, user):
        if len(v) == 0:
            v = Vote(voter=user, submission=submission)
            v.save()

    def get(self, request, id, *args, **kwargs):
        user = request.user
        isVote = 'unvote' not in request.path

        submission = Submission.objects.get(id=id)
        votes = Vote.objects.filter(submission=submission)
        v = votes.filter(voter=user)
        if isVote:
            self.vote(v, submission, user)
        else:
            self.unvote(v)

        return redirect(request.META.get('HTTP_REFERER'))


# upvoted/username view


class UpvotedView(View):

    def get(self, request, username):
        user = request.user

        try:
            user_searched = User.objects.get(username=username)

        except Exception as e:
            return HttpResponse('No such user.')

        if user != user_searched:
            return HttpResponse("Can't display that.")

        votes = Vote.objects.filter(voter=user_searched)

        submissions = []
        for vote in votes:
            vote.submission.count_comments()
            vote.submission.count_votes()
            submissions.append(vote.submission)

        context = {
            'submissions': submissions,
            'votes': votes
        }
        response = render(request, 'core/home.html', context=context)  # render the html with the context
        return HttpResponse(response)


# submit view


class SubmissionsView(View):

    def get(self, request, *args, **kwargs):
        context = {
            'submit_form': SubmissionForm(),
        }
        response = render(request, 'core/submit.html', context=context)  # render the html with the context
        return HttpResponse(response)

    def post(self, request, *args, **kwargs):
        user = request.user

        submission_form = SubmissionForm(request.POST)
        if submission_form.is_valid():
            submission_form.savedb(user)
        return redirect('news')
