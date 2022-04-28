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

    def get_serializer_class(self):
        if self.action == 'create':
            return SubmissionCreateSerializer
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

    @swagger_auto_schema(responses={202: SubmissionSerializer, 404: get_response(ResponseMessages.e404)})
    def retrieve(self, request, *args, **kwargs):
        """
            Shows submission by id

            Returns the submission by id
        """
        response = super(viewsets.ModelViewSet, self).retrieve(request, args, kwargs)
        return response

    @swagger_auto_schema(responses={202: get_response(desc="Success", message=ResponseMessages.e201_d),
                                    401: get_response(ResponseMessages.e401), 404: get_response(ResponseMessages.e404)})
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
                response_message = {'message': 'Submission has been deleted'}
                instance.delete()
                response_status = status.HTTP_202_ACCEPTED

        except Exception as e:
            response_message = {'message': ResponseMessages.e404}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={202: SubmissionSerializer, 401: get_response(ResponseMessages.e401),
                                    409: get_response(ResponseMessages.e409), 406: get_response(ResponseMessages.e406)})
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
                        return Response(response_message, status=status.HTTP_202_ACCEPTED)

                submission = standardSaveSubmission(request.user, validated_data)
                response_message = SubmissionSerializer(submission).data
                response_status = status.HTTP_202_ACCEPTED
            else:
                response_message = {'message': ResponseMessages.e406}
                response_status = status.HTTP_406_NOT_ACCEPTABLE
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
