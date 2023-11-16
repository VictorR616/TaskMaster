from django.contrib import admin

from .models import Label, Priority, Task, TaskMetadata

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
    )  


class LabelAdmin(admin.ModelAdmin):
    list_display = ("name","user")

    list_filter = ("name", "user")
    



class TaskMetadataAdmin(admin.ModelAdmin):
    list_display = (
        "task",
        "description",
        "priority",
    )

    list_filter = ("task",)


class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name","user")

    list_filter = ("name", "user")

admin.site.register(Task, TaskAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(TaskMetadata, TaskMetadataAdmin)
admin.site.register(Priority, PriorityAdmin)
