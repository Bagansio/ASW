from django.contrib.auth.models import User
from rest_framework import serializers
from server.apps.core.models import *


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    id = serializers.IntegerField(read_only=True, required=False)
    title = serializers.CharField(max_length=128, required=True)
    url = serializers.URLField(max_length=200,  required=False)
    text = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)
    votes = serializers.IntegerField(required=False)
    comments = serializers.IntegerField(required=False)

    class Meta:
        model = Submission
        fields = '__all__'


class SubmissionCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission
        fields = ['title', 'id']

class SubmissionCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Submission
        fields = ['title', 'url', 'text']



class SubmissionVoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = UserSerializer(many=False, read_only=True)
    submission = SubmissionSerializer(many=False, read_only=True)

    class Meta:
        model = Vote
        fields = '__all__'


class UserInfoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    karma = serializers.IntegerField(default=0)
    about = serializers.CharField(max_length=60000, required=False)
    email = serializers.CharField(max_length=500, required=False)
    showdead = serializers.BooleanField(default=False)
    noprocrast = serializers.BooleanField(default=False)
    maxvisit = serializers.IntegerField(default=20)
    minaway = serializers.IntegerField(default=180)
    delay = serializers.IntegerField(default=0)

    class Meta:
        model = Profile
        fields = ['user', 'karma', 'about', 'email', 'showdead', 'noprocrast', 'maxvisit', 'minaway','delay',]
