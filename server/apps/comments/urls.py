from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('<int:id>', views.CommentsView.as_view(), name='comments'),
    path('reply/<int:id>', views.replyCommentView.as_view(), name='reply'),
    path('vote/<int:id>', login_required(views.voteView.as_view()), name='voteComment'),
    path('unvote/<int:id>', login_required(views.voteView.as_view()), name='unvoteComment')
]
