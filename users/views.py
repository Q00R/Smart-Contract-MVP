
import json
from django.shortcuts import render , redirect

from rest_framework.decorators import api_view , permission_classes, parser_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Users , Documents ,Document_shared, OneTimePassword
from .serializers import DocumentSerializer ,DocumentSharedSerializer ,UserSerializer 

import secrets
import hashlib

#------new
from io import BytesIO
from django.core.files.base import ContentFile
import zipfile
from django.http import FileResponse
#----------

from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from DocuSign import settings


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
            nid = request.data['nid'],
            phone_number = request.data['phone number'],
            salt = salt
            )
        user.save()
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
# -------------------------------------------------------------------------------------------------------------
# need to be logged in
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
    
    if firstname or lastname or phone_number:
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
    
    salt = secrets.token_hex(10)
    salted_password = salt + updated_pass   
    hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()

    if hashed_password == user.password:
        return Response({'message' : 'Cannot enter an old password'}, status=status.HTTP_400_BAD_REQUEST)
    
    Users.objects.filter(user_id=pk).update(password=hashed_password, salt=salt)

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
def upload_pdf(request, pk):
    try:
        user = Users.objects.get(user_id=pk)
    except Users.DoesNotExist:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if 'document_file' in request.data:
        pdf_file = request.data['document_file']
        pdf_content = pdf_file.read()
        pdf_hash = calculate_pdf_hash(pdf_content)
        
        zip = compress_pdf_to_zip(pdf_content, pdf_file.name)
        # Create a ContentFile from the compressed content
        compressed_pdf = ContentFile(zip, name=f'{pdf_file.name}.zip')
        
        document = Documents(user=user, document_file=compressed_pdf, document_hash=pdf_hash, is_completed=False)
        document.save()
        
        return Response({'message': 'PDF uploaded and compressed successfully.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'PDF file not provided.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def get_document(request, pk):
    try:
        document = Documents.objects.get(document_id=pk)
    except Documents.DoesNotExist:
        return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    zip_buffer = BytesIO(document.document_file.read())
    with zipfile.ZipFile(zip_buffer, 'r') as zipf:
        zip_file_contents = zipf.namelist()
        
        pdf_filename = None
        for content_filename in zip_file_contents:
            if content_filename.endswith('.pdf'):
                pdf_filename = content_filename
                break
            
            if not pdf_filename:
                return Response({'message': 'PDF file not found in the ZIP.'}, status=status.HTTP_400_BAD_REQUEST)
            
        pdf_content = zipf.read(pdf_filename)
        
    response = FileResponse(BytesIO(pdf_content), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    
    return response

@api_view(['GET'])
def get_document_details(request, pk):
    try:
        document = Documents.objects.get(document_id=pk)
    except Documents.DoesNotExist:
        return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    response_data = {
            'timestamp': document.timestamp,
            'document_hash': document.document_hash,
        }
    return Response(response_data)


def compress_pdf_to_zip(pdf_content, pdf_name):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.writestr(pdf_name, pdf_content)
    return zip_buffer.getvalue()


def calculate_pdf_hash(pdf_file):
    
    sha256_hash = hashlib.sha256()
    
    sha256_hash.update(pdf_file)
    
    return sha256_hash.hexdigest()

@api_view(['GET'])
def documents_list(request, pk):
    try:
        user_documents = Documents.objects.filter(user=pk)
        shared_documents = Document_shared.objects.filter(
            owner_id=pk
        ) | Document_shared.objects.filter(parties_id=pk)
        
        user_documents_serializer = DocumentSerializer(user_documents, many=True)
        shared_documents_serializer = DocumentSharedSerializer(shared_documents, many=True)
        
        response_data = {
            "user_documents": user_documents_serializer.data,
            "shared_documents": shared_documents_serializer.data
        }
        
        return Response(response_data)
    except (Documents.DoesNotExist, Document_shared.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

# make an api/function to search on the parties and see if they have accepted or not before publishing
# make another api for sending to emails for user
# for when sending the mail put a link to accept or reject the contract