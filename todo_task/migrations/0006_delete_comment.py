# Generated by Django 4.2.5 on 2023-09-25 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_task', '0005_alter_priority_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
