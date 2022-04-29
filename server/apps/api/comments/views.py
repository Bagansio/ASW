from django.contrib.auth.models import User
from server.apps.api.core.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from server.apps.comments.utils import *
from server.apps.api.utils import *
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from server.apps.api.comments.serializers import *
from server.apps.comments.models import *



class CommentViewSet(viewsets.GenericViewSet ):
    """
    API endpoint that allows comments to be viewed or edited.
    """

    queryset = Comment.objects.all()
    serializer = CommentSerializer(queryset, many=True)
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'head', 'delete']

    def get_serializer_class(self):
        if self.action == 'reply':
            return CommentCreateSerializer
        return CommentSerializer

    @swagger_auto_schema(responses={200: CommentSerializer, 404: get_response(ResponseMessages.e404)})
    def retrieve(self, request, pk, *args, **kwargs):
        """
            Shows comment by id

            Returns the comment by id
        """
        response_status = status.HTTP_404_NOT_FOUND
        response_message = {'message': ResponseMessages.e404}

        try:
            queryset = Comment.objects.get(id=pk)
        except Exception as e:
            return Response(response_message, response_status)

        serializer = CommentSerializer(queryset, many=False)
        return Response(serializer.data)



    @swagger_auto_schema(responses={200: CommentSerializer, 404: get_response(ResponseMessages.e404)})
    @action(detail=True, methods=['GET'], name='comments')
    def comments(self, request, pk, *args, **kwargs):
        """
            Shows replies of a comment

            Returns all the replies of a comment
        """
        response_status = status.HTTP_404_NOT_FOUND
        response_message = {'message': ResponseMessages.e404}

        try:
            comment = Comment.objects.get(id=pk)
        except Exception as e:
            return Response(response_message, response_status)

        queryset = Comment.objects.filter(parent=comment)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

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
                parent = Comment.objects.get(id=pk)
            except Exception as e:
                return Response({'message': ResponseMessages.e404}, status.HTTP_404_NOT_FOUND)

            serializer = CommentCreateSerializer(data=request.data)
            if serializer.is_valid():
                reply = create_comment(request.user, serializer.validated_data['text'],
                                       parent.submission, parent.level+1, parent)
                response_message = CommentSerializer(reply).data
                response_status = status.HTTP_202_ACCEPTED

        return Response(response_message, status=response_status)

