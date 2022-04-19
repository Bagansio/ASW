from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('<int:id>', views.CommentsView.as_view(), name='comments'),
    path('reply/<int:id>', login_required(views.replyCommentView.as_view()), name='reply'),
    path('vote/<int:id>', login_required(views.voteView.as_view()), name='voteComment'),
    path('unvote/<int:id>', login_required(views.voteView.as_view()), name='unvoteComment'),

    path('threads/<str:username>', views.ThreadsView.as_view(), name='threads'),
    path('upvoted/<str:username>', views.UpvotedView.as_view(), name='upvotedComments'),

]
