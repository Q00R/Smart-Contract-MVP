from django.db import models
from django.utils import timezone 
from django import forms
import random
from datetime import timedelta

#from django.contrib.auth.models import User
#generate_key_pair generate public and private key in user model and the two fields 
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=250 , blank=False, null=True)
    lastname = models.CharField(max_length=250, blank=False, null=True)
    email = models.TextField(blank=False, null=True) #models.EmailField(unique=True)
    password =  models.TextField(blank=False, null=True)     #forms.CharField(widget=forms.PasswordInput)
    #username = models.TextField(unique=True,blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    nid = models.TextField(unique=True,blank=True, null=True)
    phone_number = models.TextField(unique=True,blank=True, null=True)
    salt = models.TextField(blank=True, null=False)
    

    class Meta:
        db_table = 'users'
        
        
    def __str__(self):
        return self.firstname
        
        
#add signature field to sign the Document with private key of owner (sign_document)
class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    document_hash = models.TextField()
    document_file = models.FileField(upload_to='documents/', null=True ,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField() 

    class Meta:
        db_table = 'documents'
        constraints = [
            models.UniqueConstraint(fields=['document_id', 'user'], name='document_user_unique')
        ]
    def __str__(self):
        return f"Document {self.document_id}"    
    



class Document_shared(models.Model):
    doc_id = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='shared_docs')
    owner_id = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='owned_docs')
    parties_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    is_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'documents_shared'
        constraints = [
            models.UniqueConstraint(fields=['doc_id', 'owner_id'], name='document_unique')
        ]

class OneTimePassword(models.Model):
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    otp = models.CharField(4)
    timestamp = models.DateTimeField(default=timezone.now)

    def generate_OTP(self):
        self.otp = str(random.randint(1000, 9999))
    
    def is_expired(self):
        new_time = self.timestamp + timedelta(minutes=2)
        if timezone.now() <= new_time:
            return False
        return True
