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
    votes = serializers.SerializerMethodField('get_votes')
    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Comment
        fields = ('id', 'submission', 'author', 'text',
                  'level', 'parent', 'created_at', 'votes', 'status')

    def get_votes(self, object):
        return len(CommentVotes.objects.filter(comment=object))


    def get_status(self, object):
        user = self.context.get('user')
        author = object.author

        if user == author:
            status = 'owner'
        else:
            votes = CommentVotes.objects.filter(voter=user).filter(comment=object)

            if len(votes) > 0:
                status = 'voted'
            else:
                status = 'unvoted'

        return status



class CommentShowVoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = UserSerializer(many=False, read_only=True)

    class Meta:
        model = CommentVotes
        fields = ('voter', )


class CommentDefaultVoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = UserSerializer(many=False, read_only=True)
    comment = CommentSerializer(many=False, read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'voter','comment']


class CommentCreateVoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = serializers.ReadOnlyField()
    comment = serializers.ReadOnlyField()

    class Meta:
        model = Vote
        fields = ['id', 'voter','comment']
