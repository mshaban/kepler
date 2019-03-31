from collections import OrderedDict

import account.forms
from django import forms
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory
from django.forms.models import ModelForm

from skill_platform.models import User
from .models import Skill, UserProfile


def validate_user_exist(kepler_id):
    if not User.objects.filter(kepler_id=kepler_id).exists():
        raise ValidationError("please make sure that your kepler id is correct")
    return kepler_id


class SignupForm(account.forms.SignupForm):
    avatar = forms.ImageField(required=True)
    kepler_id = forms.CharField(max_length=30, required=True)
    username = None
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(account.forms.SignupForm, self).__init__(*args, **kwargs)
        field_order = ["kepler_id", "first_name", "last_name", "password", "email", "avatar"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)

    class Meta:
        model = UserProfile

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean(self):
        form_data = self.cleaned_data
        kepler_id = form_data['kepler_id']
        if not User.objects.filter(kepler_id=kepler_id).exists():
            self.add_error('kepler_id', "please make sure that your kepler id is correct")
            # raise ValidationError("please make sure that your kepler id is correct")
        user = User.objects.filter(kepler_id=kepler_id).first()
        if UserProfile.objects.filter(user=user).exists():
            self.add_error('kepler_id', "Kepler profile already exists, please login")
            # raise ValidationError("Kepler profile already exists")
        email = form_data['email']
        if user and user.email != email:
            self.add_error('email', "Provided kepler id and email doesn't match")
            # raise ValidationError("Provided kepler id and email doesn't match")
        return form_data


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


class SendTokensForm(forms.Form):
    tokens = forms.FloatField()
    from_user = forms.CharField(widget=forms.HiddenInput())
    to_user = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        form_data = self.cleaned_data
        from_user = User.objects.filter(kepler_id=form_data['from_user']).first()
        to_user = User.objects.filter(kepler_id=form_data['to_user']).first()
        tokens = self.cleaned_data['tokens']
        if not from_user or not to_user:
            raise ValidationError("Cannot find specified users")
        if from_user.tokens < tokens:
            raise ValidationError("You don't have enough tokens to send")

        return form_data
