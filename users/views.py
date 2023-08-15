from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.utils import timezone 
from datetime import timedelta


from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Users , Documents ,Document_shared
from .serializers import DocumentSerializer ,DocumentSharedSerializer ,UserSerializer 

import secrets
import hashlib
import random

from django.core.mail import send_mail
from DocuSign import settings

#import meen .serializers w models     @api_view(['GET'])
#@permission_classes([IsAuthenticated]) for jwt 


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
        
    except:
        return Response({'error': 'An error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#new ---------------------------
@api_view(['GET'])    
def activate(request ,pk):
    
    user = Users.objects.get(user_id= pk)
    if not user.email:
        return Response({'error': 'Email not found'})
    
    otp = str(random.randint(1000, 9999))
    
    subject = 'Your OTP for Email Verification'
    message = f'Your OTP is: {otp}'
    recipient_list = [user.email]
    print(recipient_list)
    
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
    itime = timezone.now()
    
    print(recipient_list)
    request.session['user_otp'] = otp
    request.session['itimeOTP'] = itime
    request.session['verified_email'] = user.email
    
    return Response({'message': 'Email verification OTP sent'}, status=status.HTTP_201_CREATED)

@api_view(['POST']) 
def verify_otp(request):
#first save the time from when the otp is sent
#second check
    
    user_otps = request.data['otp']
    #user_otps = ["otp":request.data['otp'] , "Time":timezone.now]
    itiem =request.session.get("itimeOTP")
    temp = {
        "otp":user_otps,
        "time": itiem
    }
    
    new_time = temp["time"] + timedelta(minutes=1)

    
    stored_otp = request.session.get('user_otp')
    verified_email = request.session.get('verified_email')
    user = Users.objects.get(email= verified_email)
    
    print('user_otps ',temp["time"])
    print('stored_otp ',stored_otp)
    
    #if timezone.now 
    
    if timezone.now() <= new_time and temp["otp"] == stored_otp:
        print("enter time:", timezone.now() , "timedelta:" , new_time )
        user.is_activated = True
        user.save()
        request.session['user_otp'] = None
        temp = None
        return Response({'message': 'Email is Activated'})
    else:
        return Response({'error': 'OTP is not valid'})
    
    #------------------------------------------