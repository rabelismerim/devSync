from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
            raise ValueError('Superuser must have is_staff=True and is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

    def bulk_create(self, objs, batch_size=None, ignore_conflicts=False):
        raise ValueError('Bulk creation is disabled.')

    def bulk_update(self, objs, fields, batch_size=None):
        raise ValueError('Bulk update is disabled.')
