from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from server.apps.core.api.serializers import  *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Submission.objects.all().order_by('-created_at')
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
