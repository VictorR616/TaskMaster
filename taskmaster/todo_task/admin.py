from django.contrib import admin
from .models import Task, Label, Comment, TaskMetadata


# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "complete",
        "created",
    )  # Columnas que se mostrarán en la lista de registros

    list_filter = (
        "complete",
        "created",
    )  # Columnas que se mostrarán en la lista de filtros") # Columnas que se mostrarán en la lista de registros


class LabelAdmin(admin.ModelAdmin):
    list_display = ("name",)

    list_filter = ("name",)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "creation_date",
    )

    list_filter = ("creation_date",)


class TaskMetadataAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "description",
        "priority",
    )

    list_filter = ("task",)


admin.site.register(Task, TaskAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(TaskMetadata, TaskMetadataAdmin)
