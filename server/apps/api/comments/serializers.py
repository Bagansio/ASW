from django.contrib.auth.models import User
from rest_framework import serializers
from server.apps.core.models import *
from server.apps.comments.models import *
from server.apps.api.core.serializers import *



class CommentParentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('id', )

class CommentCreateSerializer(serializers.HyperlinkedModelSerializer):
    text = serializers.CharField(max_length=65535, required=True)

    class Meta:
        model = Comment
        fields = ('text', )


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)
    submission = SubmissionCommentSerializer(many=False, read_only=True)
    author = UserSerializer(many=False, read_only=True)
    text = serializers.CharField(max_length=65535, required=True)
    level = serializers.IntegerField()
    parent = CommentParentSerializer(many=False, read_only=True)
    created_at = serializers.DateTimeField(required=False)
    votes = serializers.IntegerField(required=False)


    class Meta:
        model = Comment
        fields = ('id', 'submission', 'author', 'text',
                  'level', 'parent', 'created_at', 'votes')
