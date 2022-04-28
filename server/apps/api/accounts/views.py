from django.contrib.auth.models import User
from server.apps.api.core.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from server.apps.core.utils import *
from server.apps.api.utils import *
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    http_method_names = ['get', 'head']

    @swagger_auto_schema(responses={200: SubmissionSerializer, 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='submitted')
    def submitted(self, request, pk, *args, **kwargs):
        """
            Shows the submissions submitted by given user

            Returns the user submissions
        """

        response_status = status.HTTP_404_NOT_FOUND
        response_message = {'message': ResponseMessages.e404}

        user = get_user(pk)
        if user is not None:
            queryset = Submission.objects.filter(author=user)

            serializer = SubmissionSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response(response_message, status=response_status)
