from django.contrib import admin

from .models import Task, TaskAssignee


class TaskAssigneeInline(admin.TabularInline):
    model = TaskAssignee
    extra = 0
    fields = ['user', 'task_resolved']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskAssigneeInline]
    readonly_fields = ['created_by', 'is_completed']

    @admin.display(
        boolean=True,
        description='Завершена?'
    )
    def is_completed(self, obj):
        return obj.is_completed

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
