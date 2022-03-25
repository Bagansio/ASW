from django.db import models
from ..accounts.models import User

# Create your models here.

class Submission(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, null=False)
    url = models.URLField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )

    def __str__(self):
        return 'id: ' + str(self.id) + ' title: ' + str(self.title)
