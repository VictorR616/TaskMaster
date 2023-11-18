# Generated by Django 4.2.7 on 2023-11-17 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo_task', '0025_alter_label_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='label',
            options={'ordering': ['-created'], 'verbose_name': 'Etiqueta', 'verbose_name_plural': 'Etiquetas'},
        ),
        migrations.AlterModelOptions(
            name='priority',
            options={'ordering': ['-created'], 'verbose_name': 'Prioridad', 'verbose_name_plural': 'Prioridades'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-created'], 'verbose_name': 'Tarea', 'verbose_name_plural': 'Tareas'},
        ),
        migrations.AlterField(
            model_name='label',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha y hora en que la etiqueta fue creada.', verbose_name='Fecha de Creación'),
        ),
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(help_text='Ingrese el nombre de la etiqueta.', max_length=50, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='label',
            name='user',
            field=models.ForeignKey(help_text='Usuario al que pertenece la etiqueta.', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='priority',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha y hora en que la prioridad fue creada.', verbose_name='Fecha de Creación'),
        ),
        migrations.AlterField(
            model_name='priority',
            name='name',
            field=models.CharField(help_text='Ingrese el nombre de la prioridad.', max_length=50, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='priority',
            name='user',
            field=models.ForeignKey(help_text='Usuario al que pertenece la prioridad.', on_delete=django.db.models.deletion.CASCADE, related_name='priorities', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='task',
            name='complete',
            field=models.BooleanField(default=False, help_text='Indica si la tarea está completa o no.', verbose_name='Completa'),
        ),
        migrations.AlterField(
            model_name='task',
            name='created',
            field=models.DateTimeField(auto_now_add=True, help_text='Fecha y hora en que la tarea fue creada.', verbose_name='Fecha de Creación'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(help_text='Ingrese la fecha de vencimiento.', verbose_name='Fecha de Vencimiento'),
        ),
        migrations.AlterField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(help_text='Seleccione las etiquetas asociadas a la tarea.', to='todo_task.label', verbose_name='Etiquetas'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(help_text='Ingrese el título de la tarea.', max_length=35, verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(help_text='Usuario al que pertenece la tarea.', on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='taskmetadata',
            name='description',
            field=models.TextField(help_text='Ingrese la descripción de la metadata de la tarea.', verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='taskmetadata',
            name='priority',
            field=models.ForeignKey(default=None, help_text='Seleccione la prioridad asociada a la tarea.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='todo_task.priority', verbose_name='Prioridad'),
        ),
        migrations.AlterField(
            model_name='taskmetadata',
            name='task',
            field=models.OneToOneField(help_text='Tarea a la que pertenece esta metadata.', on_delete=django.db.models.deletion.CASCADE, to='todo_task.task', verbose_name='Tarea'),
        ),
    ]