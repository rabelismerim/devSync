from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class RecordConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main.record'
    verbose_name = _("Record")
