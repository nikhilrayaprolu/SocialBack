from django.apps import AppConfig


class apiConfig(AppConfig):
    name = 'apps.api'

    def ready(self):
        import signals

