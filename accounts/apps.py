from django.apps import AppConfig

#adding the ability to create accounts for the admin
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
