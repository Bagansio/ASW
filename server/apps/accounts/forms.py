from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from datetime import timedelta
from django.utils import timezone

from .models import Profile

class ProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = ('about', 'email', 'showdead', 'noprocrast','maxvisit','minaway','delay')

    def clean(self):
        cleaned_data = self.cleaned_data

        if cleaned_data['minaway'] <0 or cleaned_data['maxvisit'] <0 or cleaned_data['delay']:
            raise ValidationError("must be positive number")
        return cleaned_data

    def savedb(self, profile):
        cleaned_data = self.cleaned_data
        if isNotNull(cleaned_data['about']):
            profile.about = cleaned_data['about']
        if isNotNull(cleaned_data['email']):
            profile.email = cleaned_data['email']
        if isNotNull(cleaned_data['showdead']):
            profile.showdead = cleaned_data['showdead']
        if isNotNull(cleaned_data['noprocrast']):
            profile.noprocrast = cleaned_data['noprocrast']
        if isNotNull(cleaned_data['maxvisit']):
            profile.maxvisit = cleaned_data['maxvisit']
        if isNotNull(cleaned_data['minaway']):
            profile.minaway = cleaned_data['minaway']
        if isNotNull(cleaned_data['delay']):
            profile.delay = cleaned_data['delay']
        profile.save()

def isNotNull(attribute):
    return attribute is not None
