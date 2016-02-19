# -*- coding: utf-8 -*-
import uuid
from django.conf import settings
from django.core.mail import send_mail as django_send_mail
from django.template.loader import render_to_string
import os


def upload_to(instance, filename):
    uid = uuid.uuid4().get_hex()
    ext = os.path.splitext(filename)[-1]
    return "uploads/{cache_1}/{cache_2}/{file_hash}{ext}".format(
        cache_1=uid[:2],
        cache_2=uid[2:4],
        file_hash=uid[4:],
        ext=ext
    )


def send_mail(subject, template_name, to, is_html=True, **kwargs):
    kwargs['settings'] = settings
    content = render_to_string(template_name, kwargs)

    django_send_mail(subject, content if not is_html else None,
                     settings.DEFAULT_FROM_EMAIL, [to],
                     html_message=content if is_html else None)