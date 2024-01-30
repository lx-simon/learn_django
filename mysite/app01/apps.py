from django.apps import AppConfig
# 【固定，不用动】

class App01Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app01'
