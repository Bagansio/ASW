from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
import datetime
from .models import Comment
from django.utils import timezone


class CommentForm(ModelForm):


    class Meta:
        model = Comment
        fields = ('text',)

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['text'] is None:
            raise ValidationError("text can't be null")
        return cleaned_data

    def savedb(self, author, submission, level, parent):

        comment = self.save(commit=False)
        comment.author = author
        comment.created_at = timezone.now()
        comment.submission = submission
        comment.level = level
        comment.parent = parent
        comment.save()
        submission.save()
        comment.auto_vote()
