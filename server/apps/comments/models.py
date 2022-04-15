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

    def __unicode__(self):
        return f'Comment of {self.submission.title} by {self.user.username}'

