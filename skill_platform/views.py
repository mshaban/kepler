from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils.decorators import method_decorator

from .forms import SkillForm, SkillFormSet
from django.urls.base import reverse_lazy

from .models import User

from .models import UserProfile
from .forms import SignupForm

from django.views.generic import FormView


# Create your views here.


@login_required
def home(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@method_decorator(login_required, name='dispatch')
class AddSkillView(FormView):
    template_name = 'skill_platform/add_skill.html'
    success_url = reverse_lazy('home')
    form_class = SkillForm

    def get_context_data(self, **kwargs):
        context = super(AddSkillView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['skills_formset'] = SkillFormSet(self.request.POST)
            kwargs['form'] = context['form']
        else:
            context['skills_formset'] = SkillFormSet()
        return context

    # def get_form_kwargs(self):
    #     kwargs = super(AddSkillView, self).get_form_kwargs()
    #     kwargs['user'] = self.request.user
    #     return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['skills_formset']
        if formset.is_valid():
            for form in formset:
                if form.is_valid():
                    skill = form.save(commit=False)
                    skill.user = self.request.user
                    skill.save()
            return super(AddSkillView, self).form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

            # def form_invalid(self, form):
            #         print(form.errors)


class SignupView(FormView):
    form_class = SignupForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('addSkill')

    def form_valid(self, form):
        kepler_id = form.cleaned_data['kepler_id']
        avatar = form.cleaned_data['avatar']
        user = User.objects.get(kepler_id=kepler_id)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.set_password(form.cleaned_data["password"])
        user.save()
        profile = UserProfile(user=user, avatar=avatar)
        profile.save()
        user = authenticate(self.request, kepler_id=kepler_id, password=form.cleaned_data["password"])
        login(self.request, user)
        return super(SignupView, self).form_valid(form)
