from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator

from .forms import SkillForm, SkillFormSet, SendTokensForm, LoginForm
from django.urls.base import reverse_lazy

from .models import User, Skill

from .models import UserProfile
from .forms import SignupForm

from django.views.generic import FormView
from django.views import generic


class SkillListView(generic.ListView):
    model = Skill
    context_object_name = 'skill_list'
    template_name = 'skill_platform/skill_list.html'


@method_decorator(login_required, name='dispatch')
class AddSkillView(FormView):
    template_name = 'skill_platform/add_skill.html'
    success_url = '/skills'
    form_class = SkillForm

    def get_context_data(self, **kwargs):
        context = super(AddSkillView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['skills_formset'] = SkillFormSet(self.request.POST)
        else:
            context['skills_formset'] = SkillFormSet()
        return context

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


class LoginView(FormView):
    form_class = LoginForm
    template_name = "account/login.html"
    success_url = '/skills'

    def form_valid(self, form):
        kepler_id = form.cleaned_data['kepler_id']
        user = authenticate(self.request, kepler_id=kepler_id, password=form.cleaned_data["password"])
        login(self.request, user)
        return super(LoginView, self).form_valid(form)


@login_required
def profile_page(request, kepler_id):
    context = {}
    if kepler_id == 'me' or kepler_id == request.user.kepler_id:
        user = request.user
        context['me'] = True
    else:
        user = User.objects.get(kepler_id=kepler_id)
        context['me'] = False
    profile = UserProfile.objects.get(user=user)
    context['user'] = user
    context['user_profile'] = profile

    # if this is a POST request we need to process the form data
    if request.method == 'POST' and not context['me']:
        form = SendTokensForm(request.POST)
        context['form'] = form
        if form.is_valid():
            token_cnt = form.cleaned_data['tokens']
            from_user = form.cleaned_data['from_user']
            to_user = form.cleaned_data['to_user']
            from_user = User.objects.filter(kepler_id=from_user).first()
            to_user = User.objects.filter(kepler_id=to_user).first()
            from_user.tokens -= token_cnt
            to_user.tokens += token_cnt
            from_user.save()
            to_user.save()
            context['tokens_sent'] = True
            context['to_user'] = "{} {}".format(to_user.first_name, to_user.last_name)
    # if a GET (or any other method) we'll create a blank form
    else:
        if not context['me']:
            to_user = kepler_id
            from_user = request.user.kepler_id
            form = SendTokensForm(initial={"from_user": from_user, "to_user": to_user, "tokens": 0})
            context['form'] = form
    return render(request, 'skill_platform/profile.html', context)
