# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('is active'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # Выше - обязательные поля
    first_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'auth_user'

    def get_absolute_url(self):
        return reverse('user:user', args=(self.pk,))

    def get_full_name(self):
        if self.first_name or self.last_name:
            return ' '.join((self.first_name, self.last_name))
        return self.email
