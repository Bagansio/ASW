from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from server.apps.api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows submissions to be viewed or edited.
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    search_fields = ['id', 'title', 'url', 'created_at', 'author']
    ordering_fields = '__all__'


class SubmissionVoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows submissions to be viewed or edited.
    """
    queryset = Vote.objects.all()
    serializer_class = SubmissionVoteSerializer
    search_fields = ['voter', 'submission']
    ordering_fields = '__all__'
