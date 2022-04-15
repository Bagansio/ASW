from django.shortcuts import render, redirect
from django.views import View
from ..core.models import Submission, Vote
from .models import Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

# Create your views here.


def get_voted(user, submission):

    if user.is_authenticated:
        votes = Vote.objects.filter(submission=submission).filter(voter=user)
        if len(votes) != 0:
            return True
    return False


class CommentsView(View):

    def load_comments(self, level, parent, submission, comments):

        childs = Comment.objects.filter(submission=submission)\
                                .filter(level=level)\
                                .filter(parent=parent)
        for child in childs:
            self.load_comments(level+1, child, submission, comments)
            comments.append(child)

    def get(self, request, id):

        user = request.user

        form = CommentForm()
        submission = Submission.objects.get(id=id)
        submission.count_votes()
        submission.count_comments()

        voted = get_voted(user, submission)
        comments = []
        self.load_comments(0, None, submission, comments)

        comments = list(reversed(comments))
        context = {
            'form': form,
            'submission': submission,
            'comments': comments,
            'voted': voted,
        }
        return render(request, 'comments/comments.html', context)

    def post(self, request, id):

        user = request.user
        form = CommentForm(request.POST)

        if form.is_valid():
            submission = Submission.objects.get(id=id)
            form.savedb(user, submission, 0)
        return redirect('comments', id=submission.id)



