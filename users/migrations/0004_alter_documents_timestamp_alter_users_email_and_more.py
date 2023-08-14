# Generated by Django 4.2.4 on 2023-08-14 13:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_users_salt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='nid',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone_number',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.TextField(blank=True, null=True, unique=True),
        ),
    ]
