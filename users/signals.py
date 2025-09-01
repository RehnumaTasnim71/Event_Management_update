from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .utils import send_activation_email

@receiver(post_save, sender=User)
def on_user_created_send_activation(sender, instance, created, **kwargs):
    if created and not instance.is_active and instance.email:
        # send email with activation link
        # Uses console backend by default
        request = None  # when created via site form, util will compute domain='localhost:8000'
        send_activation_email(instance, request)
