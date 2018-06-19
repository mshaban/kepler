import account.views
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls.base import reverse_lazy

from .models import User

from .models import UserProfile
from .forms import SignupForm

from django.views.generic import FormView, TemplateView


class SignupView(FormView):
    form_class = SignupForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('addSkill')

    def form_valid(self, form):
        kepler_id = form.cleaned_data['kepler_id']
        avatar = form.cleaned_data['avatar']
        user = User.objects.get(kepler_id=kepler_id)
        user.email = form.cleaned_data['email']
        user.password = form.cleaned_data['password']
        user.save()
        profile = UserProfile(user=user, avatar=avatar)
        profile.save()
        return super(SignupView, self).form_valid(form)

        # def after_signup(self, form):
        #     self.create_profile(form)
        #     super(SignupView, self).after_signup(form)
        # 
        # def create_profile(self, form):
        #     profile = self.created_user.userprofile  # replace with your reverse one-to-one profile attribute
        #     self.created_user.kepler_id = self.created_user.username
        #     profile.avatar = form.cleaned_data["avatar"]
        #     profile.save()
