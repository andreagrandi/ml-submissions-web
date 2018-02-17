from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    full_name = models.CharField(_('username'), max_length=255)

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_short_name(self):
        return self.email


class Submission(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    datafile = models.FileField(blank=False, null=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
