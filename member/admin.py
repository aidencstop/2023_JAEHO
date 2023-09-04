from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # list_display = ('member_id', 'is_admin',)

    list_display = ('member_id', 'is_admin', 'is_active', 'authority', 'name', 'age', 'gender', 'password', 'height')

    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('member_id',)}),
        ('Personal info', {'fields': ('name', 'age', 'gender','height',)}),
        ('Management info', {'fields': ('authority', 'password',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('member_id', 'password1', 'password2')}
         ),
    )
    search_fields = ('member_id',)
    ordering = ('member_id',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
