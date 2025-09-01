from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Event
from django.contrib.auth.models import User

@receiver(m2m_changed, sender=Event.participants.through)
def rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add' and pk_set:
        for user_id in pk_set:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                continue
            if user.email:
                send_mail(
                    subject=f"RSVP Confirmation for {instance.title}",
                    message=f"Hi {user.first_name or user.username}, you RSVP'd for {instance.title}. See you on {instance.date}.",
                    from_email="noreply@example.com",
                    recipient_list=[user.email],
                    fail_silently=True
                )
