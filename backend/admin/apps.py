from django.contrib.admin.apps import AdminConfig

class DevSyncAdminConfig(AdminConfig):
    default_site = 'admin.sites.DevSyncAdminSite'
