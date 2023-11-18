# Generated by Django 4.2.7 on 2023-11-17 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages='Este usuario ya existe', max_length=25, unique=True),
        ),
    ]