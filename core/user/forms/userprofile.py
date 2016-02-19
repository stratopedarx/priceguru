from django import forms
from django.core.exceptions import ValidationError

from core.api.models import ItemGroup


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = ItemGroup
        fields = ['group_name']

    def validate_unique(self):
        """Custom form validation, since Django didn't implement unique_together for some reason."""
        exclude = self._get_validation_exclusions()
        exclude.remove('user')  # allow checking against the missing attribute
        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e)


class AddUserItemIntoGroupForm(forms.Form):
    url = forms.URLField(required=True,
                         widget=forms.URLInput(attrs={'required': True}))
    group_id = forms.IntegerField(required=True, widget=forms.HiddenInput)
