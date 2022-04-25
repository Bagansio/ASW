from django.contrib.auth.models import User
from rest_framework import serializers
from server.apps.core.models import *


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Submission
        fields = '__all__'

class SubmissionVoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    submission = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Vote
        fields = '__all__'

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
