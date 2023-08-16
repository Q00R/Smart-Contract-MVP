from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.utils import timezone 
from datetime import timedelta


from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Users , Documents ,Document_shared, OneTimePassword
from .serializers import DocumentSerializer ,DocumentSharedSerializer ,UserSerializer 

import secrets
import hashlib
import random

from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from DocuSign import settings

#import meen .serializers w models     @api_view(['GET'])
#@permission_classes([IsAuthenticated]) for jwt 


# config ={
#     "apiKey": "AIzaSyD3WJWYnQ-tb2zettIQOKUMb6Ti9iYqfr0",
#     "authDomain": "test-16f17.firebaseapp.com",
#     "databaseURL": "https://test-16f17-default-rtdb.firebaseio.com",
#     "projectId": "test-16f17",
#     "storageBucket": "test-16f17.appspot.com",
#     "messagingSenderId": "117239109614",
#     "appId": "1:117239109614:web:c1186a8a8feb5c396860ff",
# }

# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()


@api_view(['POST'])
def register(request):
    try:
        salt = secrets.token_hex(10)
        salted_password = salt + request.data['password']
        hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
        
        user = Users.objects.create(
            email =  request.data['email'] ,
            password = hashed_password ,
            is_activated = False ,
            username = request.data['username'],
            nid = request.data['nid'],
            phone_number = request.data['phone number'],
            salt = salt
            )
        serializers = UserSerializer(user)
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])    
def activate(request, pk):
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        otpfound = OneTimePassword.objects.get(user_id = user.user_id)
        otpfound.delete()
    except OneTimePassword.DoesNotExist:
        pass  # No OTP found, nothing to delete
    
    if not user.email:
        return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    otp = OneTimePassword.objects.create(user_id = user)
    otp.generate_OTP()
    otp.save()
    
    subject = 'Your OTP for Email Verification'
    message = f'Your OTP is: {otp.otp}'
    recipient_list = [user.email]
    
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    email.send()
    
    return Response({'message': 'Email verification OTP sent'}, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def verify_otp(request, pk):
    
    user_otps = request.data.get('otp')
    if user_otps is None:
        return Response("Please provide the OTP.")
    
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user.is_activated:
        return Response("User is already activated", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if user_otps is None:
        return Response("Please provide the OTP.")
    verified_email = user.email
    user = get_object_or_404(Users, email=verified_email)
    
    try:
        saved_otp = OneTimePassword.objects.get(user_id = user.user_id)
    except OneTimePassword.DoesNotExist:
        return Response("OTP not found. Please request a new OTP.")
    
    if saved_otp.otp != user_otps:
        return Response("Invalid OTP")
    
    if saved_otp.is_expired():
        saved_otp.delete()
        return Response("OTP is expired. Please regenerate another OTP.")
    
    user.is_activated = True
    user.save()
    saved_otp.delete()
    
    return Response({'message': 'Email is Activated'})

@api_view(['PUT'])
def deactivate(request, pk):
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.is_activated:
        return Response("User is already deactivated", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    Users.objects.filter(user_id=pk).update(is_activated=False)

    return Response({'message': 'Account is deacivated'})



@api_view(['PUT'])
def EditAccount(request, pk):
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')
    username = request.data.get('username')
    #email =  request.data.get('email')
    phone_number = request.data.get('phone_number')
    
    Users.objects.filter(user_id=pk).update(firstname=firstname,username = username, lastname=lastname, phone_number=phone_number)
    
        
    return Response({'message': 'Account updated'}) 
    
    