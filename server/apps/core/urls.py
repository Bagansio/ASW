from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.news, name='main'),
    path('submit/', views.SubmissionsView.as_view(), name='submit'),
]
