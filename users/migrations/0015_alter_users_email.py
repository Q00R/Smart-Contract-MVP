# Generated by Django 4.2.4 on 2023-08-16 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_users_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.TextField(null=True),
        ),
    ]
