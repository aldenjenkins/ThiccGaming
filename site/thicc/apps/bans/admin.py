from .models import Ban, Comment, Group, Admin
from .forms import GroupForm, AdminForm
from django.contrib import admin

class BanAdmin(admin.ModelAdmin):
    list_display  = ('name', 'reason', 'created', 'length')

class CommentAdmin(admin.ModelAdmin):
    list_display  = ('created', 'comment', 'ban', 'commenter')
    raw_id_fields = ['commenter']

class GroupAdmin(admin.ModelAdmin):
    def user_count(self, obj):
        return obj.ban_group.count()

    form = GroupForm
    list_display = ('textual_name', 'name', 'flags', 'immunity', 'user_count', )


class AdminAdmin(admin.ModelAdmin):
    form = AdminForm
    list_display  = ('aid', 'user', 'authid', 'srv_group', 'srv_flags', 'immunity',)
    raw_id_fields = ['aid','srv_group']



admin.site.register(Ban, BanAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Admin, AdminAdmin)