from django.contrib import admin
from .models import Task, Label,Priority, TaskMetadata


# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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



class TaskMetadataAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "description",
        "priority",
    )

    list_filter = ("task",)


class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name",)

    list_filter = ("name",)

admin.site.register(Task, TaskAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(TaskMetadata, TaskMetadataAdmin)
admin.site.register(Priority, PriorityAdmin)
