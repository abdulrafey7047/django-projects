from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Doctor, Patient


@receiver(post_save, sender=User)
def create_user_type(sender, instance, created, **kwargs):

    try:
        user_type = instance._register_as
    except AttributeError:
        user_type = None

    if created:
        if user_type == 'doctor':
            Doctor.objects.create(user=instance)
        elif user_type == 'patient':
            Patient.objects.create(user=instance)
