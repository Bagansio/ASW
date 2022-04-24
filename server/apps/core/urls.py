from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='news'),
    path('news/', views.HomeView.as_view(), name='news'),
    path('newest/', views.NewestView.as_view(), name='newest'),
    path('ask/', views.AskView.as_view(), name='ask'),

    path('submit/', login_required(views.SubmissionsView.as_view()), name='submit'),
    path('submitted/<str:username>', views.SubmittedView.as_view(), name='submitted'),

    path('vote/<int:id>', login_required(views.voteView.as_view()), name='vote'),
    path('unvote/<int:id>', login_required(views.voteView.as_view()), name='unvote'),
    path('upvoted/<str:username>', views.UpvotedView.as_view(), name='upvoted'),

]
