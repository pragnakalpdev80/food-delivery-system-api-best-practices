from django.apps import AppConfig


class RestaurantConfig(AppConfig):
    name = 'apps.restaurants'

    def ready(self):
        pass