from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.utils import timezone
from django.db import models


class SystemUser(models.Model):
    gender_types = (
        ("M", "Male"),
        ("F", "Female"),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to="system_user_images/", null=True, blank=True)
    gender = models.CharField(max_length=1, choices=gender_types)
    birthday = models.DateField()

    class Meta:
        verbose_name = "System User"
        verbose_name_plural = "System Users"

    def __str__(self):
        return self.user.username


class SCDHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="scd_images/")
    diagnose = models.CharField(max_length=30, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "SCD History"
        verbose_name_plural = "SCD Histories"

    def __str__(self):
        return str(timezone.localtime(self.timestamp))


@receiver(post_save, sender=User)
def create_auth_token(sender, instance, created=False, *args, **kwargs):
    if created:
        Token.objects.create(user=instance)

