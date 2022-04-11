from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Submission(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, null=False)
    url = models.URLField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=False)
    votes = models.IntegerField(null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, #null because the post will exists if the user account is deleted
        null=True
    )


    def __unicode__(self):
        return self.title

    def __str__(self):
        return 'id: ' + str(self.id) + ' title: ' + str(self.title)

    def count_votes(self):
        self.votes = Vote.objects.filter(submission=self).count()

class Vote(models.Model):
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        null=False
    )
    voter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    def __unicode__(self):
        return f'{self.voter.username} voted {self.submission.title}'
