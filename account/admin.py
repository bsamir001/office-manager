# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User,Otpcode,patent
from django.contrib.auth.models import Group


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('phone_number',)}),#'password'
        ('permissions', {'fields': ('is_active', 'is_admin',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number',)}),#'password'
    )

    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.unregister(Group)
admin.site.register(User,UserAdmin)
admin.site.register(patent)
@admin.register(Otpcode)
class Otpcodeadmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created')
