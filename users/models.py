from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    name = models.CharField(_("Name of User"), blank=True, null=True, max_length=255)
    description = models.CharField(blank=True, null=True, max_length=255)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser
