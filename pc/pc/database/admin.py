from django.contrib import admin

from django.contrib import admin
from database.models import Group, Task, PC, Email, Choice, Lesson

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class PCAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpu', 'gpu', 'ram', 'id')

class EmailAdmin(admin.ModelAdmin):
    list_display = ('email', 'name')

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id',)

class LessonAdmin(admin.ModelAdmin):
    list_display= ('name', 'htmlFileName')

admin.site.register(Group, GroupAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(PC, PCAdmin)
admin.site.register(Email, EmailAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Lesson, LessonAdmin)