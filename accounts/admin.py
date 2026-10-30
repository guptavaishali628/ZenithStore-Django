from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import Account

class AccountAdmin(UserAdmin):
    #this list_display() is to display whatever the fields we want to display: 
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active') 
    # to open through the links we add to this field
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    # show you in decending order(it should be list or tuple)
    ordering=('-date_joined',)
    
    filter_horizontal=()
    list_filter = ()
    # make password readonly
    fieldsets = ()

admin.site.register(Account, AccountAdmin)