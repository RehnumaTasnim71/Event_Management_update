from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

def send_activation_email(user, request=None):
    domain = None
    if request:
        domain = get_current_site(request).domain
    if not domain:
        domain = 'localhost:8000'
    subject = 'Activate your account'
    context = {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    }
    message = render_to_string('users/activation_email.txt', context)
    send_mail(subject, message, 'noreply@example.com', [user.email])
