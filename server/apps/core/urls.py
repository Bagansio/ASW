from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.news, name='news'),
    path('submit/', views.SubmissionsView.as_view(), name='submit'),
]
