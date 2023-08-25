# Generated by Django 4.2.4 on 2023-08-25 11:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_users_username_documents_document_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.TextField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='document_shared',
            name='document_unique',
        ),
        migrations.AddField(
            model_name='document_shared',
            name='is_accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='document_shared',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_docs', to='users.users'),
        ),
        migrations.AlterField(
            model_name='documents',
            name='document_file',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.AddField(
            model_name='session',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users'),
        ),
    ]