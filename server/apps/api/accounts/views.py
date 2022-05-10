from django.contrib.auth.models import User

from server.apps.accounts.models import Profile
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


    http_method_names = ['get', 'head', 'patch']

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UserInfoSerializer
        return UserSerializer

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

    @swagger_auto_schema(responses={200: SubmissionSerializer, 401: get_response(ResponseMessages.e401), 403: get_response(ResponseMessages.e403), 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='voted_submissions')
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
    @action(detail=True, methods=['GET'], name='voted_comments')
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


    @swagger_auto_schema(responses={200: UserInfoSerializer, 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='UserInfo')
    def UserInfo(self, request, pk, *args, **kwargs):
        """
            Shows the info of given user

            Returns those info
        """

        response_status = status.HTTP_404_NOT_FOUND
        response_message = {'message': ResponseMessages.e404}
        user = get_user(pk)
        if user is not None:
            queryset = Profile.objects.filter(user=user)

            serializer = UserInfoSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

        return Response(response_message, status=response_status)


    @swagger_auto_schema(responses={200: UserInfoSerializer, 404: get_response(ResponseMessages.e404)})

    def partial_update(self, request , pk ,*args, **kwargs):
        """
            Uptdates info of given user

            Updates the info
        """
        try:
            profile = Profile.objects.get(user=request.user)

        except Exception as e:
            profile = Profile(user=request.user)
            profile.save()


        try:
            response_status = status.HTTP_401_UNAUTHORIZED
            response_message = {'message': ResponseMessages.e401}

            #user = get_user(pk)
            user = request.user
            #profile = self.getProfile(user)
            if request.user == user:

                serializer = UserInfoSerializer(data=request.data)

                if serializer.is_valid():


                    profile.about = serializer.validated_data['about']
                    profile.email = serializer.validated_data['email']
                    profile.showdead = serializer.validated_data['showdead']
                    profile.noprocrast = serializer.validated_data['noprocrast']
                    profile.maxvisit = serializer.validated_data['maxvisit']
                    profile.minaway = serializer.validated_data['minaway']
                    profile.delay = serializer.validated_data['delay']

                    #usertoupdate.save()
                    profile.save()




                    response_message = UserInfoSerializer(profile).data
                    response_status = status.HTTP_200_OK

        except Exception as e:
            response_message = {'message': ResponseMessages.e404}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, response_status)




