from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.conf import settings
from .models import *
from django.utils.translation import gettext
# Register your models here.

class DirectMailRoomAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id',"room_id",'created_on')
    fieldsets = (
        (gettext('DirectMail Info'),{'fields':('id',"room_id",'room_name','create_room_user')}),
        (gettext('Important dates'),{'fields':('created_on','updated_on',)})
    )
    search_fields = ("id","room_id","room_name","create_room_user","created_on")
    list_display = ("id","room_id","room_name","create_room_user","created_on")
    
class DMroomUserAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on')
    fieldsets = (
        (gettext('DM User Info'),{'fields':('id',"join_user","dmroom")}),
        (gettext('Important dates'),{'fields':('created_on',)})
    )
    search_fields = ("id","join_user","dmroom","created_on")
    list_display = ("id","join_user","dmroom","created_on")
    
class DirectMailMessageAdmin(ModelAdmin):
    ordering=['id']
    readonly_fields=('id','created_on')
    fieldsets = (
        (gettext('DirectMail Info'),{'fields':('id',"dm_room",'message','message_user')}),
        (gettext('Important dates'),{'fields':('created_on','updated_on',)})
    )
    search_fields = ("id","dm_room",'message','message_user',"created_on")
    list_display = ("id","dm_room",'message','message_user',"created_on")
admin.site.register(DirectMailRoom,DirectMailRoomAdmin)
admin.site.register(DMRoomJoinUser,DMroomUserAdmin)
admin.site.register(DirectMailMessage,DirectMailMessageAdmin)