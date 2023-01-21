from django.db import models
from django.core.files.storage import FileSystemStorage
from coswat.settings import IMAGES_DIR, PROFILE_PICTURES_DIR
import datetime
from django.utils.timezone import make_aware
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

picture_files_dir           = FileSystemStorage(location = IMAGES_DIR)
profile_picture_files_dir   = FileSystemStorage(location = PROFILE_PICTURES_DIR)


data_type = (
                ('Setup Data', 'Setup Data'),
                ('Calibration Data', 'Calibration Data'),
            )


class profile(models.Model):
    '''
    This is the model of a person in the community. They will be shown on the contributors page page but also will be linked with activities pages.
    '''
    user            = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)

    image           = models.ImageField(default=None, blank=True, null=True, storage = profile_picture_files_dir)

    personal_link   = models.CharField(max_length=1000, null=True, blank=True)
    location        = models.CharField(max_length=1000, null=True, blank=True)
    bio             = models.CharField(max_length=1000000, null=True, blank=True)

    date_joined     = models.DateTimeField(default = None, null=True, blank=True)
    
    reset_token     = models.CharField(max_length=1000, null=True, blank=True)
    reset_link      = models.CharField(max_length=1000, null=True, blank=True)
    token_time      = models.DateTimeField(default = None, null=True, blank=True)


    def name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    class Meta:
        ordering = ('user',)
        verbose_name = 'Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user = instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





class model_data(models.Model):

    name            = models.CharField(max_length=100000, null=False, blank=False)
    type            = models.CharField(max_length=100000, choices = data_type, default='Setup Data', null=False, blank=False)
    image           = models.ImageField(default = None, blank=False, null=False, storage = picture_files_dir)
    
    description     = models.TextField(max_length=1000000, null=False, blank=False)

    version         = models.CharField(max_length=1000, null=True, blank=True,)

    def __str__(self):
        return self.name
    class Meta:
        ordering        = ('id',)
        verbose_name    = "Model Data Source"



class welcome(models.Model):

    heading     = models.CharField(max_length=100000, null=False, blank=False)
    text        = models.TextField(max_length=100000, null=False, blank=False)

    def __str__(self):
        return self.heading
    class Meta:
        ordering        = ('id',)
        verbose_name    = "Welcome Message"




class about(models.Model):

    description     = models.TextField(max_length=100000, null=False, blank=False)
    image           = models.ImageField(default = None, blank=True, null=True, storage = picture_files_dir)

    def __str__(self):
        return 'about'
    class Meta:
        ordering        = ('id',)
        verbose_name    = "About CoSWAT-GM"

















