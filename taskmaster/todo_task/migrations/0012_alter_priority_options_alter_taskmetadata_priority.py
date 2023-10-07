# Generated by Django 4.2.5 on 2023-10-07 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo_task', '0011_alter_label_options_label_created_priority_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='priority',
            options={'ordering': ['-created'], 'verbose_name': 'Priority', 'verbose_name_plural': 'Priorities'},
        ),
        migrations.AlterField(
            model_name='taskmetadata',
            name='priority',
            field=models.ForeignKey(default='Sin Prioridad', null=True, on_delete=django.db.models.deletion.SET_NULL, to='todo_task.priority'),
        ),
    ]