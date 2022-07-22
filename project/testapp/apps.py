from django.apps import AppConfig


class TestappConfig(AppConfig):
    """Configure app"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "testapp"
