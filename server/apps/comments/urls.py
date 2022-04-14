from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('<int:id>', views.CommentsView.as_view(), name='comments')
]
