from django.shortcuts import render, redirect
from django.views import View
from ..core.models import Submission, Vote
from .models import Comment
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

# Create your views here.


class CommentsView(View):

    current_submission = None
    comments = []


    def get_voted(self, user, submission):
        if user.is_authenticated:
            votes = Vote.objects.filter(submission=submission).filter(voter=user)
            if len(votes) != 0:
                return True
        return False

    def load_comments(self,level,parent):
        childs = Comment.objects.filter(submission=self.current_submission)\
                                .filter(level=level)\
                                .filter(parent=parent)
        for child in childs:
            self.load_comments(level+1, child)
            self.comments.append(child)

    def get(self,request, id):

        user = request.user

        form = CommentForm()
        submission = Submission.objects.get(id=id)
        submission.count_votes()
        submission.count_comments()

        voted = self.get_voted(user, submission)

        current_submission = submission
        self.load_comments(0, None)

        comments = list(reversed(self.comments))
        context = {
            'form': form,
            'submission': submission,
            'comments': comments,
            'voted': voted,
        }
        print(comments)
        return render(request, 'comments/comments.html', context)

    def post(self, request, id):

        user = request.user
        form = CommentForm(request.POST)

        if form.is_valid():
            submission = Submission.objects.get(id=id)
            form.savedb(user, submission, 0)
        return redirect('comments', id=submission.id)



