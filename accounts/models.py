from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class profile (models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    about       = models.CharField(max_length=200,blank=True,null=True)
    job_title   = models.CharField( max_length=50, blank=True,null=True)
    age         = models.IntegerField(blank=True,null=True)
    image       = models.ImageField( upload_to='profile/profile_image', height_field=None, width_field=None, max_length=None, blank=True,null=True)
    joined_at   = models.DateField( auto_now=True, auto_now_add=False, blank=True,null=True)
    city        = models.ForeignKey("city", on_delete=models.CASCADE, blank=True,null=True)
    cv          = models.FileField(upload_to='profile/cv',blank=True,null=True)

    

    def __str__(self) -> str:
        return str(self.user)

class city(models.Model):
    city = models.CharField( max_length=50)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(user=instance)
