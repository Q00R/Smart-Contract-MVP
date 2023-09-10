from django.db import models
from django.utils import timezone 
from django import forms
import random
from datetime import timedelta
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
#from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User
#generate_key_pair generate public and private key in user model and the two fields 

class UsersManager(BaseUserManager):
    def _create_user(self, email, password, firstname, lastname, nid, phone_number, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        if not password:
            raise ValueError('Password is not provided')

        user = self.model(
            email = self.normalize_email(email),
            firstname = firstname,
            lastname = lastname,
            nid = nid,
            phone_number = phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, firstname, lastname, nid, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_active',False)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email, password, firstname, lastname, nid, phone_number, **extra_fields)

    def create_superuser(self, email, password, firstname, lastname, nid, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(email, password, firstname, lastname, nid, phone_number, **extra_fields)

class Users(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=250 , blank=False, null=True)
    lastname = models.CharField(max_length=250, blank=False, null=True)
    email = models.EmailField(db_index=True, unique=True, blank=False, null=True) #models.EmailField(unique=True)
     # password =  models.TextField(blank=False, null=True)     #forms.CharField(widget=forms.PasswordInput)
    nid = models.TextField(unique=True,blank=True, null=True)
    phone_number = models.TextField(unique=True,blank=True, null=True)
    
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UsersManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'nid', 'phone_number']
    

    class Meta:
        db_table = 'users'
        
        
    def __str__(self):
        return self.firstname
        
        
#add signature field to sign the Document with private key of owner (sign_document)
class Documents(models.Model):
    document_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    document_hash = models.TextField()
    document_name = models.TextField(null=True, blank=True)
    document_file = models.FileField(upload_to='documents/', null=True ,blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    is_completed = models.BooleanField() # happens when the transaction is complete on the BC

    class Meta:
        db_table = 'documents'
        constraints = [
            models.UniqueConstraint(fields=['document_id', 'user'], name='document_user_unique')
        ]
    def __str__(self):
        return f"Document {self.document_id}"    
    


class Document_shared(models.Model):
    class Acceptance(models.TextChoices):
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'
        PENDING = 'pending', 'Pending'
    doc_id = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='shared_docs')
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='owned_docs')
    parties_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    is_accepted = models.CharField(max_length=8, choices=Acceptance.choices, default=Acceptance.PENDING)
    time_a_r = models.DateTimeField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'documents_shared'

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