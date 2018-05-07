from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Skill, UserProfile


class SkillsInline(admin.TabularInline):
    model = Skill


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('kepler_id', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        # (_('Skills'), {'fields': ['skill_set']}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('kepler_id', 'password1', 'password2', 'skills'),
    #     }),
    # )
    list_display = ('kepler_id', 'first_name', 'last_name', 'is_staff')
    search_fields = ('kepler_id', 'first_name', 'last_name')
    ordering = ('kepler_id',)

    inlines = [
        SkillsInline,
    ]


models_to_register = [Skill, UserProfile]  # iterable list
admin.site.register(models_to_register)
