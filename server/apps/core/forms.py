from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
import datetime
from .models import Submission

class SubmissionForm(ModelForm):


    class Meta:
        model = Submission
        exclude = ('created_at', 'author', 'votes')




    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['title'] is None:
            raise ValidationError("Title can't be null")
        return cleaned_data


    def savedb(self,author):
        dt = datetime.datetime.now()

        submission = self.save(commit=False)
        submission.author = author
        submission.created_at = make_aware(dt)
        submission.save()


