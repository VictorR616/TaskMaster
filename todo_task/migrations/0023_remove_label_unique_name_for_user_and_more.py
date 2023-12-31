# Generated by Django 4.2.7 on 2023-11-16 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_task', '0022_label_unique_name_for_user'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='label',
            name='unique_name_for_user',
        ),
        migrations.AddConstraint(
            model_name='label',
            constraint=models.UniqueConstraint(fields=('name', 'user'), name='Categoria unica para usuario'),
        ),
        migrations.AddConstraint(
            model_name='priority',
            constraint=models.UniqueConstraint(fields=('name', 'user'), name='Prioridad unica para usuario'),
        ),
    ]
