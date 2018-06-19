"""kepler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

from skill_platform import urls, views
import account.views
from skill_platform.forms import LoginForm

urlpatterns = [
    url(r"^account/signup/$", views.SignupView.as_view(),
        name="account_signup"),
    url(r'^account/login/$',
        account.views.LoginView.as_view(
            form_class=LoginForm
        ),
        name='account_login',
        ),
    url(r"^account/", include("account.urls")),
    path('admin/', admin.site.urls),
    path('skills/', include(urls)),
]
