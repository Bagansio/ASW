from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Submission, Vote
from django.views import View
from .forms import SubmissionForm
from ..comments.models import Comment
from django.contrib.auth.models import User
from django.utils import timezone


# util functions

def get_votes(user, submission):
    if user.is_authenticated and user != submission.author:
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
        submissions = list(Submission.objects.all().order_by('-votes'))
        votes = load_submission(user, submissions)

        context = {
            'submissions': submissions,
            'votes': votes
        }
        response = render(request, 'core/home.html', context=context)  # render the html with the context
        return HttpResponse(response)

    # def post(self,request,*args,**kwargs):


#newest/ view


class NewestView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        submissions = list(Submission.objects.all().order_by('-created_at'))
        votes = load_submission(user, submissions)

        context = {
            'submissions': submissions,
            'votes': votes
        }
        response = render(request, 'core/home.html', context=context)  # render the html with the context
        return HttpResponse(response)


#ask/ view


class AskView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        submissions = list(Submission.objects.filter(url=None).order_by('-votes'))
        votes = load_submission(user, submissions)

        context = {
            'submissions': submissions,
            'votes': votes
        }
        response = render(request, 'core/home.html', context=context)  # render the html with the context
        return HttpResponse(response)




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

    def unvote(self, vote, submission):
        if len(vote) != 0:
            vote.delete()
            submission.votes = int(submission.votes) - 1
            submission.save()

    def vote(self, v, submission, user):
        if len(v) == 0:
            v = Vote(voter=user, submission=submission)
            v.save()
            submission.votes = int(submission.votes) + 1
            submission.save()

    def get(self, request, id, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            isVote = 'unvote' not in request.path

            submission = Submission.objects.get(id=id)
            votes = Vote.objects.filter(submission=submission)
            v = votes.filter(voter=user)
            if isVote:
                self.vote(v, submission, user)
            else:
                self.unvote(v, submission)

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
            if vote.voter != vote.submission.author:
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

        if user.is_authenticated:
            submission_form = SubmissionForm(request.POST)
            if submission_form.is_valid():
                url = submission_form.cleaned_data['url']
                text = submission_form.cleaned_data['text']

                if url is not None:
                    url_submissions = Submission.objects.filter(url=url)

                    if len(url_submissions) > 0: #exists another submission with url given
                        return redirect('comments', id=url_submissions[0].id)

                    if text != "":
                        submission = submission_form.urlSave(user)

                        comment = Comment(author=user, submission=submission, text=text, created_at=timezone.now(), level=0)
                        comment.save()
                        return redirect('news')

                submission_form.standardSave(user)

        return redirect('newest')
