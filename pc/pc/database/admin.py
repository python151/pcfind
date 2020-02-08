from django.contrib import admin

from django.contrib import admin
from database.models import Group, Task, PC

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class PCAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpu', 'gpu', 'ram', 'id')

admin.site.register(Group, GroupAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(PC, PCAdmin)