from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from .forms import SkillForm, SkillFormSet


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
            context['formset'] = SkillFormSet(self.request.POST, form_kwargs={'user': self.request.user})
        else:
            context['formset'] = SkillFormSet(form_kwargs={'user': self.request.user})
        return context

    def get_form_kwargs(self):
        kwargs = super(AddSkillView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
