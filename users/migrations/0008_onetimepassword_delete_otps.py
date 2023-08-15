# Generated by Django 4.2.4 on 2023-08-15 12:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_otps'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimePassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(verbose_name=4)),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2023, 8, 15, 12, 21, 1, 460509, tzinfo=datetime.timezone.utc))),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
        ),
        migrations.DeleteModel(
            name='OTPs',
        ),
    ]
