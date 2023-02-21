from django.apps import AppConfig
from django.db import OperationalError


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        try:
            from .models import MiddlewareFilter
            from .models import User

            middleware_filter, _ = MiddlewareFilter.objects.get_or_create()

            username = 'admin'
            password = 'admin'
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, password=password)

        except OperationalError:
            pass
