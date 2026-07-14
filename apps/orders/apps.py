from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = "apps.orders"

    def ready(self):
        pass
