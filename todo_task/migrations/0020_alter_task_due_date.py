# Generated by Django 4.2.7 on 2023-11-15 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_task', '0019_remove_task_labels_task_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(help_text='Ingrese la fecha de vencimiento.'),
        ),
    ]