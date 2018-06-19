from django.urls import path

from . import views

urlpatterns = [
    path('addSkill', views.AddSkillView.as_view(), name='addSkill'),
    path('', views.SkillListView.as_view(), name='skillList'),
]
