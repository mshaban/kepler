import account.forms
from django import forms
from django.forms.formsets import formset_factory

from skill_platform.models import User
from .models import Skill, UserProfile
from django.core.exceptions import ValidationError


def validate_user_exist(kepler_id):
    if not User.objects.filter(kepler_id=kepler_id).exists():
        raise ValidationError("please make sure that your kepler id is correct")
    return kepler_id

class SignupForm(account.forms.SignupForm):
    avatar = forms.ImageField(required=True)
    kepler_id = forms.CharField(max_length=30, required=True, validators=[validate_user_exist])
    username = None
    class Meta:
        model = UserProfile





class SkillForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(SkillForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Skill
        exclude = ['user']

    def save(self, commit=True):
        instance = super(SkillForm, self).save(commit=False)
        instance.user = self._user
        if commit:
            instance.save()
            self.save_m2m()
        return instance


SkillFormSet = formset_factory(form=SkillForm, max_num=5, extra=2)
