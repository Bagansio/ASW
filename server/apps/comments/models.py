from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Comment(models.Model):

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    submission = models.ForeignKey(
        'core.Submission',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    level = models.IntegerField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True
    )
    created_at = models.DateTimeField(null=False)
    votes = models.IntegerField(null=True)

    def __unicode__(self):
        return f'Comment of {self.submission.title} by {self.user.username}'

    def count_votes(self):
        self.votes = CommentVotes.objects.filter(comment=self).count()


class CommentVotes(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=False
    )
    voter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    class Meta:
        unique_together = (("comment", "voter"),) #constraint to secure the votes

    def __unicode__(self):
        return f'{self.voter.username} voted {self.comment.submission.title}'

