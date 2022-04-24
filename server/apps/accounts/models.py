from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    karma = models.IntegerField(default=0)
    about = models.TextField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length = 254,blank=True, null=True,)
    showdead = models.BooleanField(default=False)
    noprocrast = models.BooleanField(default=False)
    maxvisit = models.IntegerField(default=20)
    minaway = models.IntegerField(default=180)
    delay = models.IntegerField(default=0)

    def __unicode__(self):
        return f"{self.user}"


@receiver(post_save, sender=User)
def profile_create(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)

