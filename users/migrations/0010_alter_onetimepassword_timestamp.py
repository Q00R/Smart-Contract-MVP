# Generated by Django 4.2.4 on 2023-08-15 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_onetimepassword_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimepassword',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 13, 47, 5, 371702, tzinfo=datetime.timezone.utc)),
        ),
    ]