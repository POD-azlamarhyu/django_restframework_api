from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.conf import settings
from .models import User,UserChannel,UserManager,UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['-id']
    readonly_fields=('id',)
    list_display = ['email']
    fieldsets = (
        (_('Personal Info'), {'fields': ('id','email', 'password')}),
        (_('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login','joined_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )

class ProfileAdmin(ModelAdmin):
    ordering=['-id']
    readonly_fields=('id','created_on')
    list_display=['nickname']
    
    fieldsets = (
        (_('Personal Info'),{'fields':('id','nickname','user_profile')}),
        (_('Personal content'),{'fields':('account_id','bio','icon','link')}),
        (_('Important dates'), {'fields': ('created_on','update_at')})
    )

class ChannelAdmin(ModelAdmin):
    ordering=['-id']
    readonly_fields=('id',)
admin.site.register(User,UserAdmin)
admin.site.register(UserProfile,ProfileAdmin)
admin.site.register(UserChannel,ChannelAdmin)

