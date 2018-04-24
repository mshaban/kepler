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
from django.urls.base import reverse_lazy
from django.urls.conf import include

from skill_platform import urls, user_views, views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r"^account/signup/$", user_views.SignupView.as_view(success_url=reverse_lazy('addSkill')),
        name="account_signup"),
    url(r"^account/", include("account.urls")),
    path('admin/', admin.site.urls),
    path('skills/', include(urls)),
]
