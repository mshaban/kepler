from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


@login_required
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            kepler_id = form.cleaned_data.get('kepler_id')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(kepler_id=kepler_id, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})