import account.forms
from django import forms
from django.forms.formsets import formset_factory

from .models import Skill, UserProfile


class SignupForm(account.forms.SignupForm):
    avatar = forms.ImageField(required=True)
    kepler_id = forms.CharField(max_length=30, required=True)

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
