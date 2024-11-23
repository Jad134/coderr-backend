from django.apps import AppConfig


class OffersAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'offers_app'

    def ready(self):
        import offers_app.api.signals  