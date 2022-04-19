from django.shortcuts import render, redirect
from django.views import View
from ..core.models import Submission, Vote
from .models import Comment, CommentVotes
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.contrib.auth.models import User
from django.http import HttpResponse

# Create your views here.


class voteView(View):

    def unvote(self, vote):
        if len(vote) != 0:
            vote.delete()

    def vote(self, vote, comment, user):
        if len(vote) == 0:
            vote = CommentVotes(voter=user, comment=comment)
            vote.save()

    def get(self,request,id, *args, **kwargs):
        user = request.user
        isVote = 'unvote' not in request.path

        comment = Comment.objects.get(id=id)
        votes = CommentVotes.objects.filter(comment=comment).filter(voter=user)
        if isVote:
            self.vote(votes,comment,user)
        else:
            self.unvote(votes)

        return redirect(request.META.get('HTTP_REFERER'))


def get_voted(user, submission):

    if user.is_authenticated and user != submission.author:
        votes = Vote.objects.filter(submission=submission).filter(voter=user)
        if len(votes) != 0:
            return True
    return False


def load_comments(level, parent, submission, comments, user, votes):
    childs = Comment.objects.filter(submission=submission) \
                            .filter(parent=parent) \
                            .filter(level=level)



    for child in childs:
        load_comments(level + 1, child, submission, comments, user, votes)
        if get_votes(user, child):
            votes.append(child.id)
        comments.append(child)

def get_votes(user, comment):
    if user.is_authenticated and user != comment.author:
        v = CommentVotes.objects.filter(comment=comment).filter(voter=user)
        return len(v) != 0
    return False


class CommentsView(View):


    def get(self, request, id):

        user = request.user

        form = CommentForm()
        submission = Submission.objects.get(id=id)
        submission.count_votes()
        submission.count_comments()

        voted = get_voted(user, submission)
        comments = []
        votes = []
        load_comments(0, None, submission, comments, user, votes)

        comments = list(reversed(comments))
        context = {
            'form': form,
            'submission': submission,
            'comments': comments,
            'voted': voted,  # submission voted
            'votes': votes,  #comments voted
        }

        response = render(request, 'comments/comments.html', context)
        return HttpResponse(response)

    def post(self, request, id):

        user = request.user

        if user.is_authenticated:

            form = CommentForm(request.POST)

            if form.is_valid():
                submission = Submission.objects.get(id=id)
                form.savedb(user, submission, 0, None)

        return redirect('comments', id=id)



class replyCommentView(View):

    def get(self, request, id):
        user = request.user

        form = CommentForm()
        comment = Comment.objects.get(id=id)

        context = {
            'form': form,
            'comment': comment,
        }
        response = render(request, 'comments/reply.html', context)
        return HttpResponse(response)

    def post(self, request, id):

        user = request.user


        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment.objects.get(id=id)
            form.savedb(user, comment.submission, comment.level+1, comment)
        return redirect('comments', id=comment.submission.id)


class ThreadsView(View):


    def get(self, request, username):
        user = request.user

        try:
            user_searched = User.objects.get(username=username)

        except Exception as e:
            return HttpResponse('No such user.')

        votes = []
        comments = list(Comment.objects.filter(author=user_searched))

        for comment in comments:
            comment.level = 0
            if get_votes(user,comment):
                votes.append(comment.id)

        context = {
            'comments': comments,
            'votes': votes
        }

        response = render(request, 'comments/threads.html', context=context)  # render the html with the context
        return HttpResponse(response)

class UpvotedView(View):

    def get(self, request, username):
        user = request.user

        try:
            user_searched = User.objects.get(username=username)

        except Exception as e:
            return HttpResponse('No such user.')

        if user != user_searched:
            return HttpResponse("Can't display that.")

        votes = CommentVotes.objects.filter(voter=user_searched)

        comments = []
        for vote in votes:
            vote.comment.count_votes()
            vote.comment.level = 0
            if vote.voter != vote.comment.author:
                comments.append(vote.comment)

        context = {
            'comments': comments,
            'votes': list(votes)
        }
        response = render(request, 'comments/threads.html', context=context)  # render the html with the context
        return HttpResponse(response)
