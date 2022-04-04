from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('', views.MainView.as_view(), name='news'),
    path('submit/', login_required(views.SubmissionsView.as_view()), name='submit'),
]
