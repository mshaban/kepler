import account.views
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User

from .models import UserProfile
from .forms import SignupForm


class SignupView(account.views.SignupView):
    form_class = SignupForm

    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)

    def create_profile(self, form):
        profile = self.created_user.profile  # replace with your reverse one-to-one profile attribute
        profile.avatar = form.cleaned_data["avatar"]
        profile.save()


@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
