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
    http_method_names = ['get', 'post', 'patch', 'head', 'delete']

    def get_serializer_class(self):
        if self.action == 'reply' or self.action == 'partial_update':
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



    @swagger_auto_schema(responses={200: CommentSerializer(many=True), 404: get_response(ResponseMessages.e404)})
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
                parent = Comment.objects.get(id=pk)
            except Exception as e:
                return Response({'message': ResponseMessages.e404}, status.HTTP_404_NOT_FOUND)

            serializer = CommentCreateSerializer(data=request.data)
            if serializer.is_valid():
                reply = create_comment(request.user, serializer.validated_data['text'],
                                       parent.submission, parent.level+1, parent)
                response_message = CommentSerializer(reply).data
                response_status = status.HTTP_200_OK
            else:
                response_message = {'message': ResponseMessages.e406}
                response_status = status.HTTP_406_NOT_ACCEPTABLE

        return Response(response_message, status=response_status)

    @swagger_auto_schema(responses={200: get_response(desc="Success", message=ResponseMessages.e201_d),
                                    401: get_response(ResponseMessages.e401),
                                    404: get_response(ResponseMessages.e404)})
    def destroy(self, request, *args, **kwargs):
        """
            Deletes a comment

            Deletes a comment if request user is the author of the comment
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}
        try:
            instance = self.get_object()

            if request.user == instance.author:
                childs = Comment.objects.filter(parent=instance)
                if len(childs) == 0:
                    response_message = {'message': 'Comment has been deleted'}
                    instance.submission.comments -= 1
                    instance.submission.save()
                    instance.delete()
                    response_status = status.HTTP_200_OK
                else:
                    response_message = {'message': "ERROR: Can't delete if has replies"}
                    response_status = status.HTTP_406_NOT_ACCEPTABLE

        except Exception as e:
            response_message = {'message': ResponseMessages.e404}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, status=response_status)


    def partial_update(self, request, *args, **kwargs):
        """
            Deletes a comment

            Deletes a comment if request user is the author of the comment
        """
        response_status = status.HTTP_401_UNAUTHORIZED
        response_message = {'message': ResponseMessages.e401}
        try:
            instance = self.get_object()
            if request.user == instance.author:
                serializer = CommentCreateSerializer(data=request.data)
                if serializer.is_valid():
                    instance.text = serializer.validated_data['text']
                    instance.save()

                    response_message = CommentSerializer(instance).data
                    response_status = status.HTTP_200_OK
                else:
                    response_message = {'message': ResponseMessages.e406}
                    response_status = status.HTTP_406_NOT_ACCEPTABLE
        except Exception as e:
            response_message = {'message': ResponseMessages.e404}
            response_status = status.HTTP_404_NOT_FOUND

        return Response(response_message, response_status)
