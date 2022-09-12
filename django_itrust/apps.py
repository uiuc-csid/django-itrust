from django.apps import AppConfig


class DjangoITrust(AppConfig):
    name = "django_itrust"
    default_auto_field = "django.db.models.AutoField"
    default = True

    def ready(self):
        # from django.conf import settings
        # from . import app_settings as defaults

        # for name in dir(defaults):
        #     if name.isupper() and not hasattr(settings, name):
        #         setattr(settings, name, getattr(defaults, name))

        pass
