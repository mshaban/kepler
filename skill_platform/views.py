from django.http.response import HttpResponse
from django.shortcuts import render
import account.views
import account.decorators
# Create your views here.


@account.decorators.login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class SignupView(account.views.SignupView):

    def after_signup(self, form):
        self.update_profile(form)
        super(SignupView, self).after_signup(form)

    def update_profile(self, form):
        profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
        # profile.kepler_id = form.cleaned_data['kepler_id']
        # profile.skills = form.cleaned_data['skills']
        profile.save()