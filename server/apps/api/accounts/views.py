from django.contrib.auth.models import User

from server.apps.api.comments.serializers import CommentSerializer
from server.apps.api.core.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from server.apps.comments.models import CommentVotes
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
    @action(detail=True, methods=['GET'], name='submissions')
    def submissions(self, request, pk, *args, **kwargs):
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

    @swagger_auto_schema(responses={200: SubmissionSerializer, 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='comments')
    def comments(self, request, pk, *args, **kwargs):
        """
            Shows the submissions submitted by given user

            Returns the user submissions
        """

        response_status = status.HTTP_404_NOT_FOUND
        response_message = {'message': ResponseMessages.e404}

        user = get_user(pk)
        if user is not None:
            queryset = Comment.objects.filter(author=user)

            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={200: SubmissionSerializer, 401: get_response(ResponseMessages.e401), 403: get_response(ResponseMessages.e403), 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='voted-submissions')
    def voted_submission(self, request, pk):
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}

        user = get_user(pk)
        if request.user.is_authenticated:
            if user is not None:
                if request.user == user:
                    votes = Vote.objects.filter(voter=user)
                    submissions = []
                    for vote in votes:
                        if vote.voter != vote.submission.author:
                            submissions.append(vote.submission)

                    serializer = SubmissionSerializer(submissions, many=True)
                    return Response(serializer.data)
                else:
                    response_message = {'message': ResponseMessages.e403}
                    response_status = status.HTTP_403_FORBIDDEN
            else:
                response_message = {'message': ResponseMessages.e404}
                response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={200: SubmissionSerializer, 401: get_response(ResponseMessages.e401),
                                    403: get_response(ResponseMessages.e403),
                                    404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='voted-comments')
    def voted_comments(self, request, pk):
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}

        user = get_user(pk)
        if request.user.is_authenticated:
            if user is not None:
                if request.user == user:
                    votes = CommentVotes.objects.filter(voter=user)
                    '''votes = Vote.objects.filter(voter=user)'''
                    comments = []
                    for vote in votes:
                        if vote.voter != vote.comment.author:
                            comments.append(vote.comment)

                    serializer = CommentSerializer(comments, many=True)
                    return Response(serializer.data)
                else:
                    response_message = {'message': ResponseMessages.e403}
                    response_status = status.HTTP_403_FORBIDDEN
            else:
                response_message = {'message': ResponseMessages.e404}
                response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, status=response_status)
