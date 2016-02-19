# -*- coding: utf-8 -*-
from core.user.models import User
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import (UserCreationForm as DjangoUserCreationForm,
                                       UserChangeForm as DjangoUserChangeForm)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=32,
                               widget=forms.TextInput(
                               attrs={
                                      'class': 'form-control',
                                      'placeholder': _("Username"),
                                      'style': "width: 350px;"
                                      }),
                               required=True,
                               label=''

                               )
    password = forms.CharField(max_length=32,
                               widget=forms.PasswordInput(
                               attrs={
                                    'class': 'form-control',
                                    'placeholder': _("Password"),
                                    'style': "width: 350px;"
                                    }),
                               required=True,
                               label='')


class RegisterForm(forms.ModelForm):
    password =forms.CharField(max_length=32,
                               widget=forms.PasswordInput(
                               attrs={
                                    'class': 'form-control',
                                    'placeholder': _("Password"),
                                    'style': "width: 350px;"
                                    }),
                               required=True,
                               label='')
    required_css_class = 'required'

    class Meta:
        exclude = ['date_joined', 'last_login',
                   'is_active', 'is_staff', 'is_superuser',
                   'first_name', 'last_name',
                   'groups', 'user_permissions']
        model = get_user_model()
        labels = {
            'username': '',
            'email': '',
        }
        widgets = {
            'username': forms.TextInput(
                               attrs={
                                    'class': 'form-control',
                                    'placeholder': _("Username"),
                                    'style': "width: 350px;"
                                    }),
            'email': forms.TextInput(
                               attrs={
                                    'class': 'form-control',
                                    'placeholder': _("Email"),
                                    'style': "width: 350px;"
                                    }),
        }


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = User
        fields = ("username",)


class UserChangeForm(DjangoUserChangeForm):

    class Meta:
        model = User
        exclude = ('date_joined',)


def exists_user_by_email(email):
    from django.core.exceptions import ObjectDoesNotExist
    try:
        get_user_model().objects.get(email=email)
    except ObjectDoesNotExist, e:
        raise ValidationError(_("User does not exists"))


class RestorePasswordRequestForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
                               attrs={
                                      'class': 'form-control',
                                      'placeholder': _("Your email"),
                                      'style': "width: 350px;"
                                      }),
                               label='',
                             validators=[exists_user_by_email])
