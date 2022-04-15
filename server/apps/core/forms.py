from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from datetime import timedelta
from django.utils import timezone

from .models import Submission

class SubmissionForm(ModelForm):


    class Meta:
        model = Submission
        fields = ('title', 'url', 'text', )




    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['title'] is None:
            raise ValidationError("Title can't be null")
        return cleaned_data


    def savedb(self,author):
        dt = timezone.now()

        submission = self.save(commit=False)
        submission.author = author
        submission.created_at = timezone.now()
        submission.save()


