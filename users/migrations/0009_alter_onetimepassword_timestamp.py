# Generated by Django 4.2.4 on 2023-08-15 12:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_onetimepassword_delete_otps'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimepassword',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 15, 12, 22, 0, 445001, tzinfo=datetime.timezone.utc)),
        ),
    ]