# Create your views here.

import account.views

import kepler_platform.forms


class SignupView(account.views.SignupView):
    form_class = kepler_platform.forms.SignupForm
    identifier_field = 'email'

    def generate_username(self, form):
        # do something to generate a unique username (required by the
        # Django User model, unfortunately)
        username = "<magic>"
        return username
