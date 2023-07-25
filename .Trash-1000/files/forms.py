from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from orchestra.core import validators
from orchestra.contrib.systemusers.models import WebappUsers
from .models import WebApp


class WebappCreationForm(forms.ModelForm):
    username = forms.CharField(label=_("Username"), max_length=16,
        required=False, validators=[validators.validate_name],
        help_text=_("Required. 16 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain 16 characters or fewer, only letters, numbers and "
                         "@/./+/-/_ characters.")})
    user = forms.ModelChoiceField(required=False, queryset=WebappUsers.objects)
    password1 = forms.CharField(label=_("Password"), required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'off'}),
        validators=[validators.validate_password])
    password2 = forms.CharField(label=_("Password confirmation"), required=False,
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = WebApp
        fields = ('username', 'account', 'type')

    def __init__(self, *args, **kwargs):
        super(WebappCreationForm, self).__init__(*args, **kwargs)
    

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = _("The two password fields didn't match.")
            raise ValidationError(msg)
        return password2
