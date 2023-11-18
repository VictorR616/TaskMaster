# Generated by Django 4.2.5 on 2023-10-07 15:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo_task', '0009_task_user_alter_task_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='priority',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='priorities', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]