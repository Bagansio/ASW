from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('<str:username>', views.ProfileView.as_view(), name='profile'),
]
