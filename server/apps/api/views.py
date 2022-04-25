from django.contrib.auth.models import User
from server.apps.api.serializers import *
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from server.apps.core.models import  *
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404


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
    serializer = SubmissionSerializer(queryset, many=True)
    serializer_class = SubmissionSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ['author', 'created_at', 'votes']
    search_fields = ('title', 'url')
    http_method_names = ['get', 'post', 'head', 'delete']

    def list(self, request, *args, **kwargs):
        """
            Show submissions

            Return the submissions

            You can order by 'author' , 'created_at' and 'votes'.
            Also if want a reverse order add a "-" prefix.

            Search by 'title' or 'url'
        """
        response = super(viewsets.ModelViewSet, self).list(request, args, kwargs)
        return response

    def retrieve(self, request, *args, **kwargs):
        """
            Show submission by id

            Returns the submission by id
        """
        response = super(viewsets.ModelViewSet, self).retrieve(request, args, kwargs)
        return response

    def destroy(self, request, *args, **kwargs):
        """
            Deletes a submission

            Deletes a submission if request user is the author of the submission
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': 'not authorized'}
        try:
            instance = self.get_object()
            if request.user == instance.author:
                response_message = {'message': 'Submission has been deleted'}
                instance.delete()
                response_status = status.HTTP_202_ACCEPTED

        except Exception as e:
            response_message = {'message': 'not found'}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, status=response_status)



class SubmissionVoteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows submissions to be viewed or edited.
    """
    queryset = Vote.objects.all()
    serializer_class = SubmissionVoteSerializer
    search_fields = ['voter', 'submission']
    ordering_fields = '__all__'


class Post_APIView(APIView):

    def get(self, request, format=None, *args, **kwargs):

        if request.user.is_authenticated:
            submissions = Submission.objects.filter(author=request.user)
            serializer_context = {
                'request': request,
            }
            serializer = SubmissionSerializer(submissions, context=serializer_context, many=True)
            print(submissions)
            return Response(serializer.data)
        data = {'message': 'not authenticated'}
        return Response(data, status.HTTP_406_NOT_ACCEPTABLE)
