
import json
from django.shortcuts import render , redirect, HttpResponse
from django.http import HttpRequest

from rest_framework.decorators import api_view , permission_classes, parser_classes, authentication_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

# from users.middleware import get_session_token , custom_auth_required


from .models import Users , Documents ,Document_shared, OneTimePassword 
from .serializers import DocumentSerializer ,DocumentSharedSerializer ,UserSerializer  

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
# from rest_framework_jwt.views import obtain_jwt_token


#lama y3mel logout delelte token
#fadel nzbat lw 3mal kaza login my3odsh y3mel create le token kaza mara 

# make an api/function to search on the parties and see if they have accepted or not before publishing
# make another api for sending emails for user
# for when sending the mail put a link to accept or reject the contract


@api_view(['POST'])
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
# @login_required
# @api_view(['GET'])    
# def activate(request):
    
#     session_key = request.COOKIES.get('sessionid')
#     session = Session.objects.filter(session_key=session_key, expire_date__gte=timezone.now()).first()

#     if session is None:
#         return Response({'error': 'Invalid session'}, status=status.HTTP_401_UNAUTHORIZED)

#     user_id = session.get_decoded().get('_auth_user_id')

#     try:
#         user = Users.objects.get(pk=user_id)
#     except Users.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     if user.is_active:
#         return Response({'Message': 'User already activated'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     try:
#         otpfound = OneTimePassword.objects.get(user_id = user.user_id)
#         otpfound.delete()
#     except OneTimePassword.DoesNotExist:
#         pass  # No OTP found, nothing to delete
    
#     if not user.email:
#         return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
    
#     otp = OneTimePassword.objects.create(user_id = user)
#     otp.generate_OTP()
#     otp.save()
    
    
#     subject = 'Your OTP for Email Verification'
#     message = f'Your OTP is: {otp.otp}'
#     recipient_list = [user.email]
#     print("user.email: " , user.email)
#     email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
#     print("Sending email: " , settings.EMAIL_HOST_USER)
#     print("Sending email pass: " , settings.EMAIL_HOST_PASSWORD)



#     try:
#         email.send() 
#         return Response({'message': 'Email verification OTP sent'}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def activate(request):
    user = request.user

    # Rest of your activation logic
    # ...

    if user.is_active:
        return Response({'Message': 'User already activated'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    try:
        otpfound = OneTimePassword.objects.get(user_id=user.user_id)
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
# @api_view(['PUT'])
# def verify_otp(request):
    
#     user_otps = request.data.get('otp')
#     if user_otps is None:
#         return Response("Please provide the OTP.")
    
#     data = getUser(request)
#     user = data.data["user"]
    
#     if user.is_active:
#         return Response("User is already activated", status=status.HTTP_405_METHOD_NOT_ALLOWED)

#     if user_otps is None:
#         return Response("Please provide the OTP.")
#     verified_email = user.email
#     user = get_object_or_404(Users, email=verified_email)
    
#     try:
#         saved_otp = OneTimePassword.objects.get(user_id = user.user_id)
#     except OneTimePassword.DoesNotExist:
#         return Response("OTP not found. Please request a new OTP.")
    
#     if saved_otp.otp != user_otps:
#         return Response("Invalid OTP")
    
#     if saved_otp.is_expired():
#         saved_otp.delete()
#         return Response("OTP is expired. Please regenerate another OTP.")
    
#     user.is_active = True
#     user.save()
#     saved_otp.delete()
    
#     return Response({'message': 'Email is Activated'})

# deactivate account
# @custom_auth_required
# @api_view(['PUT'])
# def deactivate(request):
    
#     data = getUser(request)
#     user = data.data["user"]
    
#     if not user.is_active:
#         return Response("User is already deactivated", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
#     Users.objects.filter(user_id=user.user_id).update(is_active=False)

#     return Response({'message': 'Account is deacivated'})
# -------------------------------------------------------------------------------------------------------------

# edit account
# @custom_auth_required
# @api_view(['PUT'])
# def EditAccount(request):

#     user = getUser(request)
#     data = user.data["user"]

#     firstname = request.data.get('firstname')
#     lastname = request.data.get('lastname')

#     phone_number = request.data.get('phone_number')
   
#     # add some defensive programming
    
#     if firstname or lastname or phone_number:
#         res = Users.objects.filter(user_id=data.user_id).update(firstname=firstname, lastname=lastname, phone_number=phone_number)
        
        
#     return Response({'message': 'Account updated'}) 

# @custom_auth_required
# @api_view(['GET'])    
# def email_pass_reset(request):
    
#     data = getUser(request)
#     user = data.data["user"]

#     try:
#         otpfound = OneTimePassword.objects.get(user_id = user.user_id)
#         otpfound.delete()
#     except OneTimePassword.DoesNotExist:
#         pass  # No OTP found, nothing to delete
    
#     if not user.email:
#         return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)
    
#     otp = OneTimePassword.objects.create(user_id = user)
#     otp.generate_OTP()
#     otp.save()
    
    
#     subject = 'Your OTP for Password reset'
#     message = f'Your OTP is: {otp.otp}'
#     recipient_list = [user.email]
#     print("user.email: " , user.email)
#     email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
    
#     try:
#         email.send() 
#         return Response({'message': 'Password reset OTP sent'}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# reset password
# # @custom_auth_required
# @api_view(['PUT'])
# def reset_password(request):
    
#     data = getUser(request)
#     user = data.data["user"]

    
#     user_otps = request.data.get('otp')
#     if user_otps is None:
#         return Response("Please provide the OTP.")
    
#     if user_otps is None:
#         return Response("Please provide the OTP.")
#     verified_email = user.email
#     user = get_object_or_404(Users, email=verified_email)
   
#     updated_pass = request.data.get('password') #request.data['password']
#     if updated_pass is None:
#         return Response("Please provide the NEW Password.")
    
#     try:
#         saved_otp = OneTimePassword.objects.get(user_id = user.user_id)
#     except OneTimePassword.DoesNotExist:
#         return Response("OTP not found. Please request a new OTP.")
    
#     if saved_otp.otp != user_otps:
#         return Response("Invalid OTP")
    
#     if saved_otp.is_expired():
#         saved_otp.delete()
#         return Response("OTP is expired. Please regenerate another OTP.")
    
    
    
#     salt = secrets.token_hex(10)
#     salted_password = salt + updated_pass   
#     hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()

#     if hashed_password == user.password:
#         return Response({'message' : 'Cannot enter an old password'}, status=status.HTTP_400_BAD_REQUEST)
    
#     Users.objects.filter(user_id=user.user_id).update(password=hashed_password, salt=salt)
#     saved_otp.delete()
    
#     sessionToken = Session.objects.get(user_id=user)
#     sessionToken.delete()

#     return Response({'message': 'Password Reset'})

@api_view(['POST'])
@permission_classes([AllowAny])
def log_in(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request=request, email=email, password=password)
    print("user:", user)
    if user is not None:
        # # request = HttpRequest(request)
        # login(request, user=user)
        # # token = obtain_jwt_token(user)
        # return Response({'session': request.session, 'session_key' : request.session.session_key}, status=status.HTTP_202_ACCEPTED)
        referesh = RefreshToken.for_user(user)
        access_token = str(referesh.access_token)
        return Response({'access_token' : access_token}, status=status.HTTP_200_OK)
    else:
        return Response({'message' : 'invalid login'}, status=status.HTTP_400_BAD_REQUEST)    

# # @custom_auth_required
# @api_view(['POST'])
# def logout(request):
    
#     data = getUser(request)
#     user = data.data["user"]

#     try:
#         token = Session.objects.filter(user_id=user)
#         token.delete()
#     except Session.DoesNotExist:
#         # redirect to login page
#         pass

#     return Response({'message : You are logged out'}, status=status.HTTP_200_OK)

# @custom_auth_required
# @api_view(['POST'])
# def upload_pdf(request):
#     message = ''
    
#     data = getUser(request)
#     user = data.data["user"]
    
#     if 'document_file' in request.data:
#         pdf_file = request.data['document_file']
#         pdf_content = pdf_file.read()
#         pdf_hash = calculate_pdf_hash(pdf_content)
        
#         zip = compress_pdf_to_zip(pdf_content, pdf_file.name)
#         # Create a ContentFile from the compressed content
#         compressed_pdf = ContentFile(zip, name=f'{pdf_file.name}.zip')
#         print("pdf_file.name: " , pdf_file.name)
#         try:
#             existdoc= Documents.objects.filter(user=user, document_hash=pdf_hash)
#             if existdoc:
#                 return Response({'message': 'File already uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
#         except Documents.DoesNotExist:
#             pass
#         document = Documents(user=user, document_file=compressed_pdf, document_hash=pdf_hash, is_completed=False)
#         document.save()
                
#         if 'email_list' in request.data:
#             list_of_gmail = request.get["email_list"] 
#             for email in list_of_gmail:
#                 print("email: " , email)
#                 try:
#                     party = Users.objects.get(email=email)
#                 except Users.DoesNotExist:
#                     return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
#                 doc_shared = Document_shared(doc_id=document, owner_id = user, parties_id = party)
#                 try:
#                     exist_ds = Document_shared.objects.filter(doc_id=document, owner_id = user, parties_id = party)
#                     if exist_ds:
#                         message += f'Email {party.email} was already added'
#                         continue
#                 except Document_shared.DoesNotExist:
#                     pass
#                 doc_shared.save()
                
#         return Response({'message': 'PDF uploaded and compressed successfully.' + message}, status=status.HTTP_201_CREATED)
#     else:
        return Response({'message': 'PDF file not provided.'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# # @custom_auth_required
# def get_document(request, pk):

    
#     data = getUser(request)
#     user = data.data["user"]
#     try:
#         document = Documents.objects.get(document_id=pk, user=user)
#     except Documents.DoesNotExist:
#         return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
        
#     zip_buffer = BytesIO(document.document_file.read())
#     with zipfile.ZipFile(zip_buffer, 'r') as zipf:
#         zip_file_contents = zipf.namelist()
        
#         pdf_filename = None
#         for content_filename in zip_file_contents:
#             if content_filename.endswith('.pdf'):
#                 pdf_filename = content_filename
#                 break
            
#             if not pdf_filename:
#                 return Response({'message': 'PDF file not found in the ZIP.'}, status=status.HTTP_400_BAD_REQUEST)
            
#         pdf_content = zipf.read(pdf_filename)
        
#     response = FileResponse(BytesIO(pdf_content), content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{pdf_filename}"'
    
#     return response

# @api_view(['GET'])
# # @custom_auth_required
# def get_document_details(request, pk):
    
#     data = getUser(request)
#     user = data.data["user"]
#     try:
#         document = Documents.objects.get(document_id=pk, user=user)
#     except Documents.DoesNotExist:
#         return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
    
#     response_data = {
#             'timestamp': document.timestamp,
#             'document_hash': document.document_hash,
#         }
#     return Response(response_data)


# def compress_pdf_to_zip(pdf_content, pdf_name):
#     zip_buffer = BytesIO()
#     with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         zipf.writestr(pdf_name, pdf_content)
#     return zip_buffer.getvalue()


# def calculate_pdf_hash(pdf_file):
    
#     sha256_hash = hashlib.sha256()
    
#     sha256_hash.update(pdf_file)
    
#     return sha256_hash.hexdigest()


# @api_view(['GET'])
# def example_api(request):
#     data = {'message': 'Hello from Django API!!!'}
#     return Response(data)
# @api_view(['GET'])
# # @custom_auth_required
# def documents_list(request):

#     data = getUser(request)
#     user = data.data["user"]

#     try:
#         user_documents = Documents.objects.filter(user=user)
#         shared_documents = Document_shared.objects.filter(
#             owner_id=user
#         ) | Document_shared.objects.filter(parties_id=user)
        
#         user_documents_serializer = DocumentSerializer(user_documents, many=True)
#         shared_documents_serializer = DocumentSharedSerializer(shared_documents, many=True)
        
#         response_data = {
#             "user_documents": user_documents_serializer.data,
#             "shared_documents": shared_documents_serializer.data
#         }
        
#         return Response(response_data)
#     except (Documents.DoesNotExist, Document_shared.DoesNotExist):
#         return Response(status=status.HTTP_404_NOT_FOUND)

# @api_view(['PUT'])
# # @custom_auth_required
# def reject_document(request, doc_id):
#     data = getUser(request)
#     user = data.data["user"]
#     try:
#         docsh_id = Document_shared.objects.get(doc_id=doc_id, parties_id=user)
#     except Document_shared.DoesNotExist:
#         return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     docsh_id.is_accepted = False
#     docsh_id.save()
#     return Response({'message' : 'Document rejected'}, status=status.HTTP_202_ACCEPTED)


# @api_view(['PUT'])
# # @custom_auth_required
# def confirm_document(request, doc_id):
#     data = getUser(request)
#     user = data.data["user"]
#     try:
#         doc = Document_shared.objects.get(doc_id = doc_id , parties_id=user)
#     except Documents.DoesNotExist:
#         return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
    
#     doc.is_accepted = True
#     doc.save()
    
#     return Response({'message': 'Document accepted'}, status=status.HTTP_200_OK)


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
# @api_view(['GET'])
# def get_confirmation(request, doc_id):
#     data = getUser(request)
#     user = data.data["user"]
#     try:
#         docs = Document_shared.objects.filter(doc_id = doc_id , owner_id=user)
#     except Documents.DoesNotExist:
#         return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
    
#     accept = False
#     for document in docs:
#         if document.is_accepted:
#             accept = True
#         else:
#             accept = False
#             break
    
#     if accept:
#         acc_docs = DocumentSharedSerializer(docs, many=True)
#         return Response({'message : All other parties have accepted', acc_docs}, status=status.HTTP_200_OK)
    
#     r_docs = Document_shared.objects.filter(doc_id=doc_id, owner_id=user, is_accepted=False)
#     rej_docs = DocumentSharedSerializer(r_docs, many=True)
#     return Response({'message : Not all other parties have accepted', rej_docs}, status=status.HTTP_200_OK)

