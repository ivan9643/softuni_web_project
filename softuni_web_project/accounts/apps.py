from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'softuni_web_project.accounts'

    def ready(self):
        import softuni_web_project.accounts.signals