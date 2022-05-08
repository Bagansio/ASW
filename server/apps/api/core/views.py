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
from server.apps.api.comments.serializers import *
from server.apps.comments.utils import *


class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows submissions to be viewed or edited.
    """

    queryset = Submission.objects.all()
    serializer = SubmissionSerializer(queryset, many=True)
    serializer_class = SubmissionSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ['author', 'created_at', 'votes', 'comments']
    search_fields = ('title', 'url')
    http_method_names = ['get', 'post', 'head', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return SubmissionCreateSerializer
        elif self.action == 'reply':
            return CommentCreateSerializer
        elif self.action == 'vote':
            return SubmissionCreateVoteSerializer
        return SubmissionSerializer

    def list(self, request, *args, **kwargs):
        """
            Shows submissions

            Returns the submissions

            You can order by 'author' , 'created_at' and 'votes'.
            Also if want a reverse order add a "-" prefix.

            Search by 'title' or 'url'
        """
        response = super(viewsets.ModelViewSet, self).list(request, args, kwargs)
        return response

    @swagger_auto_schema(responses={200: SubmissionSerializer, 404: get_response(ResponseMessages.e404)})
    def retrieve(self, request, *args, **kwargs):
        """
            Shows submission by id

            Returns the submission by id
        """
        response = super(viewsets.ModelViewSet, self).retrieve(request, args, kwargs)
        return response

    @swagger_auto_schema(responses={200: get_response(desc="Success", message=ResponseMessages.e201_d),
                                    401: get_response(ResponseMessages.e401),
                                    404: get_response(ResponseMessages.e404)})
    def destroy(self, request, *args, **kwargs):
        """
            Deletes a submission

            Deletes a submission if request user is the author of the submission
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}
        try:
            instance = self.get_object()
            if request.user == instance.author:
                if instance.comments == 0:
                    response_message = {'message': 'Submission has been deleted'}
                    instance.delete()
                    response_status = status.HTTP_200_OK
                else:
                    response_message = {'message': "ERROR: Can't delete if has comments"}
                    response_status = status.HTTP_406_NOT_ACCEPTABLE

        except Exception as e:
            response_message = {'message': ResponseMessages.e404}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={200: SubmissionSerializer,
                                    401: get_response(ResponseMessages.e401),
                                    409: get_response(ResponseMessages.e409),
                                    406: get_response(ResponseMessages.e406)})
    def create(self, request, *args, **kwargs):
        """
            Creates a submission

            Creates a submission if request user is authenticated
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}
        if request.user.is_authenticated:
            serializer = SubmissionCreateSerializer(data=request.data)
            if serializer.is_valid():

                validated_data = serializer.validated_data

                url = validated_data['url']
                text = validated_data['text']

                if url is not None:

                    message = already_exists(Submission.objects.filter(url=validated_data['url']),
                                             'submission', 'url', request)
                    if message is not None:
                        return Response(message, status=status.HTTP_409_CONFLICT)

                    if text is not None and text != "":
                        submission = urlSaveSubmission(request.user, validated_data)

                        comment = Comment(author=request.user, submission=submission, text=text,
                                          created_at=timezone.now(),
                                          level=0)
                        comment.save()
                        response_message = SubmissionSerializer(submission).data
                        return Response(response_message, status=status.HTTP_200_OK)

                submission = standardSaveSubmission(request.user, validated_data)
                response_message = SubmissionSerializer(submission).data
                response_status = status.HTTP_200_OK
            else:
                response_message = {'message': ResponseMessages.e406}
                response_status = status.HTTP_406_NOT_ACCEPTABLE
        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={200: CommentSerializer, 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='comments')
    def comments(self, request, pk, *args, **kwargs):
        """
            Shows comments of a submission

            Returns all the comments of a submission
        """
        response_status = status.HTTP_404_NOT_FOUND
        response_message = {'message': ResponseMessages.e404}

        try:
            submission = Submission.objects.get(id=pk)
        except Exception as e:
            return Response(response_message, response_status)

        queryset = Comment.objects.filter(submission=submission)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: CommentSerializer,
                                    401: get_response(ResponseMessages.e401),
                                    404: get_response(ResponseMessages.e404)})
    @comments.mapping.post
    def reply(self, request, pk, *args, **kwargs):
        """
           Creates a reply of a comment

           Creates a new reply of a comment
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}
        if request.user.is_authenticated:
            try:
                submission = Submission.objects.get(id=pk)
            except Exception as e:
                return Response({'message': ResponseMessages.e404}, status.HTTP_404_NOT_FOUND)

            serializer = CommentCreateSerializer(data=request.data)
            if serializer.is_valid():
                reply = create_comment(request.user, serializer.validated_data['text'],
                                       submission, 0, None)
                response_message = CommentSerializer(reply).data
                response_status = status.HTTP_200_OK

        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={200: SubmissionVoteSerializer(many=True), 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='votes')
    def votes(self, request, pk, *args, **kwargs):
        """
           Shows votes of a submission by id

            Returns all the votes of a submission
        """
        response_status = status.HTTP_404_NOT_FOUND
        response_message = {'message': ResponseMessages.e404}
        submission = Submission.objects.get(id=pk)
        if submission is not None:
            queryset = Vote.objects.filter(submission=submission)

            serializer = SubmissionVoteSerializer(queryset, many=True)
            return Response(serializer.data)

        return Response(response_message, status=response_status)


    @swagger_auto_schema(responses={200: SubmissionSerializer,
                                    401: get_response(ResponseMessages.e401),
                                    404: get_response(ResponseMessages.e404),
                                    409: get_response(ResponseMessages.e409)})
    @votes.mapping.post
    def vote(self, request, pk, *args, **kwargs):
        """
           Votes a submission

           Upvotes a given submission
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}
        if request.user.is_authenticated:
            try:
                submission = Submission.objects.get(id=pk)
            except Exception as e:
                return Response({'message': ResponseMessages.e404}, status.HTTP_404_NOT_FOUND)

            votes = Vote.objects.filter(submission=submission).filter(voter=request.user)
            if len(votes) == 0:

                vote = saveSubmissionVote(request.user, submission)
                response_message = SubmissionDefaultVoteSerializer(vote).data
                response_status = status.HTTP_200_OK

            else:
                response_message = {'message': ResponseMessages.e409}
                response_status = status.HTTP_409_CONFLICT
        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={200: get_response(desc="Success", message=ResponseMessages.e201_d),
                                    401: get_response(ResponseMessages.e401),
                                    404: get_response(ResponseMessages.e404)})
    @votes.mapping.delete
    def destroy_vote(self, request, pk, *args, **kwargs):
        """
            Deletes a vote

            Deletes a vote if request user is its author
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}
        if request.user.is_authenticated:

            submission = Submission.objects.get(id=pk)
            if submission is not None:

                votes = Vote.objects.filter(submission=submission).filter(voter=request.user)
                if len(votes) != 0:
                    vote = votes[0]
                    if submission.author != request.user or request.user == vote.voter:
                        deletesubmissionVote(vote, submission)

                        response_status = status.HTTP_200_OK
                        response_message = {'message': ResponseMessages.s200}
                    else:
                        response_status = status.HTTP_403_FORBIDDEN
                        response_message = {'message': ResponseMessages.e403}

                else:
                    response_message = {'message': ResponseMessages.e404}
                    response_status = status.HTTP_404_NOT_FOUND
                # request.user != instance.author
                # not exists vote
                #

            else:
                response_message = {'message': ResponseMessages.e404}
                response_status = status.HTTP_404_NOT_FOUND


        return Response(response_message, status=response_status)


    '''
    @votes.mapping.post
    def vote(self, request, pk, *args, **kwargs):
    """
       Shows votes of a submission by id

        Returns all the votes of a submission
    """
    '''
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
