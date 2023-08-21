from PyPDF2 import PdfFileReader
from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.utils import timezone 
from datetime import timedelta


from rest_framework.decorators import api_view , permission_classes, parser_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import FileUploadParser


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

# register account
@api_view(['POST'])
def register(request):
    try:
        salt = secrets.token_hex(10)
        salted_password = salt + request.data['password']
        hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
        
        user = Users.objects.create(
            email =  request.data['email'] ,
            password = hashed_password ,
            firstname = request.data['firstname'],
            lastname = request.data['lastname'],
            is_activated = False ,
            #username = request.data['username'],
            nid = request.data['nid'],
            phone_number = request.data['phone number'],
            salt = salt
            )
        serializers = UserSerializer(user)
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# send mail with activation
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
    print("user.email: " , user.email)
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
    try:
        email.send() 
        return Response({'message': 'Email verification OTP sent'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# verify acc with otp
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

# deactivate account
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


# edit account
@api_view(['PUT'])
def EditAccount(request, pk):
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')
    #username = request.data.get('username')
    #email =  request.data.get('email')
    phone_number = request.data.get('phone_number')
   
    # add some defensive programming
    
    Users.objects.filter(user_id=pk).update(firstname=firstname, lastname=lastname, phone_number=phone_number)
    
        
    return Response({'message': 'Account updated'}) 
    

# reset password
@api_view(['PUT'])
def reset_password(request,pk):
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    updated_pass = request.data.get('password') #request.data['password']
    
    if updated_pass is None:
        return Response("Please provide the NEW Password.")
    
    salt = user.salt
    salted_password = salt + updated_pass   
    hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
    
    Users.objects.filter(user_id=pk).update(password=hashed_password)

    return Response({'message': 'Password Reset'})


# login
@api_view(['POST'])
def login(request):
    
    email = request.data.get('email')
    password = request.data.get('password')
    
    if email is None or password is None:
        if email is None:
            return Response({'error': 'Please Enter Email '}, status=status.HTTP_412_PRECONDITION_FAILED)
        elif password is None:
            return Response({'error': 'Please Enter Password '}, status=status.HTTP_412_PRECONDITION_FAILED)

    
    try:
        user = Users.objects.get(email=email) 
    except Users.DoesNotExist:
        return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
    
    salt = user.salt
    salted_password = salt + password
    hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()
    
    if hashed_password == user.password:
        return Response("Login successful")
    else:
        return Response("incorrect password, please try again.")
    
@api_view(['POST'])
#@parser_classes([FileUploadParser])
def upload_pdf(request, pk):
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    #print("request.data: ", request.data)
    if 'document_file' in request.data:
        pdf_file = request.data['document_file']
        
        pdf_content = pdf_file.read()
        # Calculate the hash of the PDF file
        pdf_hash = calculate_pdf_hash(pdf_content)
        
        document = Documents(user=user, document_file=pdf_file, document_hash=pdf_hash, is_completed=False)
        document.save()
        return Response({'message': 'PDF uploaded successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'PDF file not provided.'}, status=status.HTTP_400_BAD_REQUEST)


def calculate_pdf_hash(pdf_file):
    
    sha256_hash = hashlib.sha256()
    
    sha256_hash.update(pdf_file)
    
    return sha256_hash.hexdigest()


@api_view(['GET'])
def example_api(request):
    data = {'message': 'Hello from Django API!!!'}
    return Response(data)