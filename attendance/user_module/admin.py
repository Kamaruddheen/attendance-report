from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('username','email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_type')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'user_type', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name','user_type')
    ordering = ('username', 'user_type', )


# class StaffModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'is_hod']


# admin.site.register(StaffModel, StaffModelAdmin)