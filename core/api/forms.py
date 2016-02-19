# -*- coding: utf-8 -*-
from django import forms



class AddUrlForm(forms.Form):
    url = forms.URLField(required=True)
