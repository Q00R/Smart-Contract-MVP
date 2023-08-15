from django.db import models
from django.utils import timezone 
from django import forms

#from django.contrib.auth.models import User

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = forms.CharField(widget=forms.PasswordInput)
    username = models.TextField(unique=True,blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    nid = models.TextField(unique=True,blank=True, null=True)
    phone_number = models.TextField(unique=True,blank=True, null=True)
    salt = models.TextField(blank=True, null=False)

    class Meta:
        db_table = 'users'
        
        

class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    document_hash = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField()

    class Meta:
        db_table = 'documents'
        constraints = [
            models.UniqueConstraint(fields=['document_id', 'user'], name='document_user_unique')
        ]



class Document_shared(models.Model):
    doc_id = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='shared_docs')
    owner_id = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='owned_docs')
    parties_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'documents_shared'
        constraints = [
            models.UniqueConstraint(fields=['doc_id', 'owner_id'], name='document_unique')
        ]

