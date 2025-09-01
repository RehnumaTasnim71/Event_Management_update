# from django.apps import AppConfig

# class UsersConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'users'

#     def ready(self):
#         # Ensure groups exist and connect signals
#         from django.contrib.auth.models import Group
#         for name in ['Admin', 'Organizer', 'Participant']:
#             Group.objects.get_or_create(name=name)
#         import users.signals  # noqa

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'