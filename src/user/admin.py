from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import Account

class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_field = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    readonly_fields = ('date_joined', 'last_login')
    
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, UserAdmin)