from django.contrib.auth.models import User
from rest_framework import serializers
from server.apps.core.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionVoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = UserSerializer(many=False, read_only=True)
    submission = SubmissionSerializer(many=False, read_only=True)

    class Meta:
        model = Vote
        fields = '__all__'

