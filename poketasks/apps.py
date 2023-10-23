from django.apps import AppConfig


class PoketasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poketasks'

    def ready(self):
        import poketasks.signals
