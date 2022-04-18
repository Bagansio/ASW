from django.shortcuts import render, redirect
from django.views import View
from ..core.models import Submission, Vote
from .models import Comment, CommentVotes
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

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



class CommentsView(View):

    def load_comments(self, level, parent, submission, comments, user, votes):

        childs = Comment.objects.filter(submission=submission)\
                                .filter(level=level)\
                                .filter(parent=parent)
        for child in childs:
            self.load_comments(level+1, child, submission, comments, user, votes)
            if self.get_votes(user, child):
                votes.append(child.id)
            comments.append(child)

    def get_votes(self, user, comment):
        if user.is_authenticated and user != comment.author:
            v = CommentVotes.objects.filter(comment=comment).filter(voter=user)
            return len(v) != 0
        return False

    def get(self, request, id):

        user = request.user

        form = CommentForm()
        submission = Submission.objects.get(id=id)
        submission.count_votes()
        submission.count_comments()

        voted = get_voted(user, submission)
        comments = []
        votes = []
        self.load_comments(0, None, submission, comments, user, votes)

        comments = list(reversed(comments))
        context = {
            'form': form,
            'submission': submission,
            'comments': comments,
            'voted': voted,  # submission voted
            'votes': votes,  #comments voted
        }

        return render(request, 'comments/comments.html', context)

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
        return render(request, 'comments/reply.html', context)


    def post(self, request, id):

        user = request.user


        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment.objects.get(id=id)
            form.savedb(user, comment.submission, comment.level+1, comment)
        return redirect('comments', id=comment.submission.id)
