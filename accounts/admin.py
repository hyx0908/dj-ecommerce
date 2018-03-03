from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import (UserAdminChangeForm, UserAdminCreationForm)
from .models import GuestEmail, EmailVerification

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'first_name', 'last_name', 'admin')
    list_filter = ('admin', 'staff', 'is_active')
    readonly_fields = ('date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_joined')}),
        ('Permissions', {'fields': ('admin', 'staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']

    class Meta:
        model = User


admin.site.register(GuestEmail)
admin.site.register(EmailVerification)
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
