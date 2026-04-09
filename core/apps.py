from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from django.contrib.auth.models import User

        username_field = User._meta.get_field("username")
        username_field.validators = []
        username_field.help_text = ""
