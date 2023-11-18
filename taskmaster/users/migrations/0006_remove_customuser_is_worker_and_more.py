# Generated by Django 4.2.5 on 2023-10-31 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_worker',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(default='users/images/profile_pictures/default.png', upload_to='users/images/profile_pictures/'),
        ),
    ]