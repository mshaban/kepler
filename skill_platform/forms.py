from django import forms
import account.forms
from .models import UserProfile


class SignupForm(account.forms.SignupForm):
    avatar = forms.ImageField(required=True)

    class Meta:
        model = UserProfile