from django import forms
from django.forms.widgets import Textarea

import account.forms


class SignupForm(account.forms.SignupForm):

    skills = forms.Textarea()
    kepler_id = forms.CharField()
    