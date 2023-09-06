# Generated by Django 4.2.4 on 2023-09-04 14:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=250, null=True)),
                ('lastname', models.CharField(max_length=250, null=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('password', models.TextField(null=True)),
                ('is_activated', models.BooleanField(default=False)),
                ('nid', models.TextField(blank=True, null=True, unique=True)),
                ('phone_number', models.TextField(blank=True, null=True, unique=True)),
                ('salt', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.TextField(blank=True, null=True, unique=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
        ),
        migrations.CreateModel(
            name='OneTimePassword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(verbose_name=4)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('document_id', models.AutoField(primary_key=True, serialize=False)),
                ('document_hash', models.TextField()),
                ('document_name', models.TextField(blank=True, null=True)),
                ('document_file', models.FileField(blank=True, null=True, upload_to='documents/')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_completed', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
            options={
                'db_table': 'documents',
            },
        ),
        migrations.CreateModel(
            name='Document_shared',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=8)),
                ('time_a_r', models.DateTimeField(blank=True, default=None, null=True)),
                ('doc_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_docs', to='users.documents')),
                ('owner_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_docs', to='users.users')),
                ('parties_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.users')),
            ],
            options={
                'db_table': 'documents_shared',
            },
        ),
        migrations.AddConstraint(
            model_name='documents',
            constraint=models.UniqueConstraint(fields=('document_id', 'user'), name='document_user_unique'),
        ),
    ]
