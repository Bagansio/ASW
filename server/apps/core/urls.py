from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='news'),
    path('submit/', login_required(views.SubmissionsView.as_view()), name='submit'),
    path('vote/<int:id>', login_required(views.voteView.as_view()), name='vote'),
    path('unvote/<int:id>', login_required(views.voteView.as_view()), name='unvote'),

    path('submitted/<str:username>', views.SubmittedView.as_view(), name='submitted')
]
