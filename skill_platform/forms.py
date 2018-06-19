from collections import OrderedDict

import account.forms
from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import ModelForm

from skill_platform.models import User
from .models import Skill, UserProfile
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def validate_user_exist(kepler_id):
    if not User.objects.filter(kepler_id=kepler_id).exists():
        raise ValidationError("please make sure that your kepler id is correct")
    return kepler_id


class SignupForm(account.forms.SignupForm):
    avatar = forms.ImageField(required=True)
    kepler_id = forms.CharField(max_length=30, required=True, validators=[validate_user_exist])
    username = None
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)

    def __init__(self, *args, **kwargs):
        super(account.forms.SignupForm, self).__init__(*args, **kwargs)
        field_order = ["kepler_id", "first_name", "last_name", "password", "password_confirm", "avatar"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)

    class Meta:
        model = UserProfile


class LoginForm(account.forms.LoginForm):
    kepler_id = forms.CharField(label=("kepler_id"))
    username = None
    identifier_field = "kepler_id"
    authentication_fail_message = ("The email address and/or password you specified are not correct.")

    def __init__(self, *args, **kwargs):
        super(account.forms.LoginForm, self).__init__(*args, **kwargs)
        field_order = ["kepler_id", "password", "remember"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)

    class Meta:
        model = User


class SkillForm(ModelForm):
    name = forms.CharField(max_length=100, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Skill
        exclude = ['user']


SkillFormSet = formset_factory(form=SkillForm)
