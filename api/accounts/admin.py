from django.contrib import admin
from django.conf import settings
from .models import User,UserChannel,UserManager,UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _


class UserAdmin(BaseUserAdmin):
    ordering = ['-id']
    readonly_fields=('id',)
    list_display = ['email']
    fieldsets = (
        (None, {'fields': ('id','email', 'password')}),
        (_('Personal Info'), {'fields': ()}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email','password1','password2')
        }),
    )

class ProfileAdmin(BaseUserAdmin):
    ordering=['-id']
    readonly_fields=('id',)
    list_display=['nickname']
    

class ChannelAdmin(BaseUserAdmin):
    pass
admin.site.register(User,UserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserChannel)

