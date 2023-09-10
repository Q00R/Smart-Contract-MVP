
import json
from django.shortcuts import render , redirect, HttpResponse
from django.http import HttpRequest

from rest_framework.decorators import api_view , permission_classes, parser_classes, authentication_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

# from users.middleware import get_session_token , custom_auth_required


from .models import Users , Documents ,Document_shared, OneTimePassword 
from .serializers import DocumentSerializer ,DocumentSharedSerializer ,UserSerializer, MyTokenObtainPairSerializer

import secrets
import hashlib

#------new
from io import BytesIO
from django.core.files.base import ContentFile
import zipfile
from django.http import FileResponse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.sessions.models import Session

#--------

from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from DocuSign import settings
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from DocuSign.authentication import CustomJWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
# from rest_framework_jwt.views import obtain_jwt_token



#lama y3mel logout delelte token
#fadel nzbat lw 3mal kaza login my3odsh y3mel create le token kaza mara 

# make an api/function to search on the parties and see if they have accepted or not before publishing
# make another api for sending emails for user
# for when sending the mail put a link to accept or reject the contract


@api_view(['POST'])
# @permission_classes([AllowAny])
def register(request):
    try:
		
        User = get_user_model()
        newuser = User.objects._create_user(
            email =  request.data['email'] ,
            password = request.data['password'] ,
            firstname = request.data['firstname'],
            lastname = request.data['lastname'],
            nid = request.data['nid'],
            phone_number = request.data['phone number'],
            )
        newuser.save()
        return Response({'message': 'User created'}, status=status.HTTP_201_CREATED) 
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# send mail with activation
@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def activate(request):
    user = request.user

    if user.is_active:
        return Response({'Message': 'User already activated'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        otpfound = OneTimePassword.objects.get(user_id=user.id)
        otpfound.delete()
    except OneTimePassword.DoesNotExist:
        pass  # No OTP found, nothing to delete

    if not user.email:
        return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)

    otp = OneTimePassword.objects.create(user_id=user)
    otp.generate_OTP()
    otp.save()

    subject = 'Your OTP for Email Verification'
    message = f'Your OTP is: {otp.otp}'
    recipient_list = [user.email]
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)

    try:
        email.send()
        return Response({'message': 'Email verification OTP sent'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# verify acc with otp
# @custom_auth_required
@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def verify_otp(request):
    
    user_otps = request.data.get('otp')
    if user_otps is None:
        return Response("Please provide the OTP.")
    
    user = request.user

    if user.is_active:
        return Response("User is already activated", status=status.HTTP_405_METHOD_NOT_ALLOWED)

    if user_otps is None:
        return Response("Please provide the OTP.")
    verified_email = user.email
    user = get_object_or_404(Users, email=verified_email)
    
    try:
        saved_otp = OneTimePassword.objects.get(user_id = user.id)
    except OneTimePassword.DoesNotExist:
        return Response("OTP not found. Please request a new OTP.")
    
    if saved_otp.otp != user_otps:
        return Response("Invalid OTP")
    
    if saved_otp.is_expired():
        saved_otp.delete()
        return Response("OTP is expired. Please regenerate another OTP.")
    
    user.is_active = True
    user.save()
    saved_otp.delete()
    
    return Response({'message': 'Email is Activated'})

# deactivate account
# @custom_auth_required
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@authentication_classes([IsAuthenticated])
def deactivate(request):
    
    user = request.user    
    Users.objects.filter(pk=user.id).update(is_active=False)

    return Response({'message': 'Account is deacivated'})
# -------------------------------------------------------------------------------------------------------------

# edit account
# @custom_auth_required
@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def EditAccount(request):

    user = request.user

    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')

    phone_number = request.data.get('phone_number')
   
    # add some defensive programming
    
    if firstname or lastname or phone_number:
        res = Users.objects.filter(pk=user.id).update(firstname=firstname, lastname=lastname, phone_number=phone_number)
        
        
    return Response({'message': 'Account updated'}) 

# @custom_auth_required
@api_view(['GET'])   
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated]) 
def email_pass_reset(request):
    
    user = request.user
    try:
        otpfound = OneTimePassword.objects.get(user_id = user.id)
        otpfound.delete()
    except OneTimePassword.DoesNotExist:
        pass  # No OTP found, nothing to delete
    
    if not user.email:
        return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    otp = OneTimePassword.objects.create(user_id = user)
    otp.generate_OTP()
    otp.save()
    
    
    subject = 'Your OTP for Password reset'
    message = f'Your OTP is: {otp.otp}'
    recipient_list = [user.email]
    print("user.email: " , user.email)
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
    try:
        email.send() 
        return Response({'message': 'Password reset OTP sent'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# reset password
# # @custom_auth_required
@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def reset_password(request):
    
    user = request.user
    
    user_otps = request.data.get('otp')
    if user_otps is None:
        return Response("Please provide the OTP.")
    
    if user_otps is None:
        return Response("Please provide the OTP.")
    verified_email = user.email
    user = get_object_or_404(Users, email=verified_email)
   
    updated_pass = request.data.get('password') #request.data['password']
    if updated_pass is None:
        return Response("Please provide the NEW Password.")
    
    try:
        saved_otp = OneTimePassword.objects.get(user_id = user.id)
    except OneTimePassword.DoesNotExist:
        return Response("OTP not found. Please request a new OTP.")
    
    if saved_otp.otp != user_otps:
        return Response("Invalid OTP")
    
    if saved_otp.is_expired():
        saved_otp.delete()
        return Response("OTP is expired. Please regenerate another OTP.")
    
    if user.check_password(updated_pass):
        return Response({'message' : 'Cannot enter an old password'}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(updated_pass)

    saved_otp.delete()
    
    return Response({'message': 'Password Reset'}, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
@permission_classes([AllowAny])
def log_in(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request=request, email=email, password=password)
    if user is not None:
        serializer = MyTokenObtainPairSerializer()
        tokens = serializer.get_token(user)
        access_token = tokens.access_token
        refresh = tokens
        # refresh = RefreshToken.for_user(user)
        # access_token = refresh.access_token

        # Set token expiration time
        access_token.set_exp(from_time=timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])
        
        # Access the custom claims from the token payload
        user_id = access_token.payload.get('user_id')
        firstname = access_token.payload.get('firstname')
        lastname = access_token.payload.get('lastname')
        email = access_token.payload.get('email')
        nid = access_token.payload.get('nid')
        phone_number = access_token.payload.get('phone_number')
        is_active = access_token.payload.get('is_active')
        return Response({ 
        'message': 'login successful',
        "token" :{
            'refresh': str(refresh),
            'access': str(access_token),},
        "user":{
            'user_id' : user_id,
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'nid': nid,
            'phone_number': phone_number,
        },
            'is_active': is_active,
    }, status=status.HTTP_200_OK)
    else:
        return Response({'message' : 'invalid login'}, status=status.HTTP_400_BAD_REQUEST)    

# # @custom_auth_required
@api_view(['POST'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    
    user = request.user
    try:
        token = Session.objects.filter(user_id=user)
        token.delete()
    except Session.DoesNotExist:
        # redirect to login page
        pass

    return Response({'message : You are logged out'}, status=status.HTTP_200_OK)

# @custom_auth_required
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_pdf(request):
    message = ''
    
    user = request.user
    if 'document_file' in request.data:
        pdf_file = request.data['document_file']
        pdf_content = pdf_file.read()
        pdf_hash = calculate_pdf_hash(pdf_content)
        
        zip = compress_pdf_to_zip(pdf_content, pdf_file.name)
        # Create a ContentFile from the compressed content
        compressed_pdf = ContentFile(zip, name=f'{pdf_file.name}.zip')
        print("pdf_file.name: " , pdf_file.name)
        try:
            existdoc= Documents.objects.filter(user=user, document_hash=pdf_hash)
            if existdoc:
                return Response({'message': 'File already uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        except Documents.DoesNotExist:
            pass
        document = Documents(user=user, document_file=compressed_pdf, document_hash=pdf_hash, is_completed=False)
        document.save()
                
        if 'email_list' in request.data:
            list_of_gmail = request.get["email_list"] 
            for email in list_of_gmail:
                print("email: " , email)
                try:
                    party = Users.objects.get(email=email)
                except Users.DoesNotExist:
                    return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
                doc_shared = Document_shared(doc_id=document, owner_id = user, parties_id = party)
                try:
                    exist_ds = Document_shared.objects.filter(doc_id=document, owner_id = user, parties_id = party)
                    if exist_ds:
                        message += f'Email {party.email} was already added'
                        continue
                except Document_shared.DoesNotExist:
                    pass
                doc_shared.save()
                
        return Response({'message': 'PDF uploaded and compressed successfully.' + message}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'PDF file not provided.'}, status=status.HTTP_400_BAD_REQUEST)


# # @custom_auth_required
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_document(request, pk):

    user = request.user
    try:
        document = Documents.objects.get(document_id=pk, user=user)
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

# # @custom_auth_required
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_document_details(request, pk):
    user = request.user
    try:
        document = Documents.objects.get(document_id=pk, user=user)
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
def example_api(request):
    data = {'message': 'Hello from Django API!!!'}
    return Response(data)
# # @custom_auth_required
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def documents_list(request):
    user = request.user

    try:
        user_documents = Documents.objects.filter(user=user)
        shared_documents = Document_shared.objects.filter(
            owner_id=user
        ) | Document_shared.objects.filter(parties_id=user)
        
        user_documents_serializer = DocumentSerializer(user_documents, many=True)
        shared_documents_serializer = DocumentSharedSerializer(shared_documents, many=True)
        
        response_data = {
            "user_documents": user_documents_serializer.data,
            "shared_documents": shared_documents_serializer.data
        }
        
        return Response(response_data)
    except (Documents.DoesNotExist, Document_shared.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

# # @custom_auth_required
@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def reject_document(request, doc_id):
    user = request.user
    try:
        docsh_id = Document_shared.objects.get(doc_id=doc_id, parties_id=user)
    except Document_shared.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    
    docsh_id.is_accepted = False
    docsh_id.save()
    return Response({'message' : 'Document rejected'}, status=status.HTTP_202_ACCEPTED)


# # @custom_auth_required
@api_view(['PUT'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def confirm_document(request, doc_id):
    user = request.user
    try:
        doc = Document_shared.objects.get(doc_id = doc_id , parties_id=user)
    except Documents.DoesNotExist:
        return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    doc.is_accepted = True
    doc.save()
    
    return Response({'message': 'Document accepted'}, status=status.HTTP_200_OK)


# def getUser(request):
#     sessionToken = get_session_token(request)
#     #ser = SessionSerializer(sessionToken)
#     #print("sessionToken: " , sessionToken.token)
#     try:
#         print("d5lt el try")
#         session = Session.objects.get(token=sessionToken.data)
#         user = Users.objects.get(user_id=session.user_id_id)
        
#         return Response({"user": user})
#     except Session.DoesNotExist:
#         return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    
# # @custom_auth_required
@api_view(['GET'])
@authentication_classes([CustomJWTAuthentication])
@permission_classes([IsAuthenticated])
def get_confirmation(request, doc_id):
    user = request.user
    try:
        docs = Document_shared.objects.filter(doc_id = doc_id , owner_id=user)
    except Documents.DoesNotExist:
        return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    accept = False
    for document in docs:
        if document.is_accepted:
            accept = True
        else:
            accept = False
            break
    
    if accept:
        acc_docs = DocumentSharedSerializer(docs, many=True)
        return Response({'message : All other parties have accepted', acc_docs}, status=status.HTTP_200_OK)
    
    r_docs = Document_shared.objects.filter(doc_id=doc_id, owner_id=user, is_accepted=False)
    rej_docs = DocumentSharedSerializer(r_docs, many=True)
    return Response({'message : Not all other parties have accepted', rej_docs}, status=status.HTTP_200_OK)

