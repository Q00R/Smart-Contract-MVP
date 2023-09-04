
import json
from django.shortcuts import render , redirect

from rest_framework.decorators import api_view , permission_classes, parser_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from users.middleware import get_session_token , custom_auth_required


from .models import Users , Documents ,Document_shared, OneTimePassword , Session
from .serializers import DocumentSerializer ,DocumentSharedSerializer ,UserSerializer  , SessionSerializer

import secrets
import hashlib

#------new
from io import BytesIO
from django.core.files.base import ContentFile
import zipfile
from django.http import FileResponse
#--------

from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from DocuSign import settings
from django.utils import timezone 
from django.urls import reverse


#lama y3mel logout delete token
#fadel nzbat lw 3mal kaza login my3odsh y3mel create le token kaza mara 

# make an api/function to search on the parties and see if they have accepted or not before publishing
# make another api for sending emails for user
# for when sending the mail put a link to accept or reject the contract


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
@custom_auth_required
@api_view(['GET'])    
def activate(request):
    
    data = getUser(request)
    user = data.data["user"]
    
    if user.is_activated:
        return Response({'Message': 'User already activated'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
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
    # print("user.email: " , user.email)
    email = EmailMessage(subject, message, from_email= settings.EMAIL_HOST_USER, to=recipient_list)
    # print("Sending email: " , settings.EMAIL_HOST_USER)
    # print("Sending email pass: " , settings.EMAIL_HOST_PASSWORD)



    try:
        email.send() 
        return Response({'message': 'Email verification OTP sent'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# verify acc with otp
@custom_auth_required
@api_view(['PUT'])
def verify_otp(request):
    
    user_otps = request.data.get('otp')
    if user_otps is None:
        return Response("Please provide the OTP.")
    
    data = getUser(request)
    user = data.data["user"]
    
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
@custom_auth_required
@api_view(['PUT'])
def deactivate(request):
    
    data = getUser(request)
    user = data.data["user"]
    
    if not user.is_activated:
        return Response("User is already deactivated", status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    Users.objects.filter(user_id=user.user_id).update(is_activated=False)

    return Response({'message': 'Account is deacivated'})
# -------------------------------------------------------------------------------------------------------------

# edit account
@custom_auth_required
@api_view(['PUT'])
def EditAccount(request):

    user = getUser(request)
    data = user.data["user"]

    firstname = request.data.get('firstname')
    lastname = request.data.get('lastname')

    phone_number = request.data.get('phone_number')
   
    # add some defensive programming
    
    if firstname or lastname or phone_number:
        res = Users.objects.filter(user_id=data.user_id).update(firstname=firstname, lastname=lastname, phone_number=phone_number)
        
        
    return Response({'message': 'Account updated'}) 

@custom_auth_required
@api_view(['GET'])    
def email_pass_reset(request):
    
    data = getUser(request)
    user = data.data["user"]

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
@custom_auth_required
@api_view(['PUT'])
def reset_password(request):
    
    data = getUser(request)
    user = data.data["user"]

    
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
        saved_otp = OneTimePassword.objects.get(user_id = user.user_id)
    except OneTimePassword.DoesNotExist:
        return Response("OTP not found. Please request a new OTP.")
    
    if saved_otp.otp != user_otps:
        return Response("Invalid OTP")
    
    if saved_otp.is_expired():
        saved_otp.delete()
        return Response("OTP is expired. Please regenerate another OTP.")
    
    
    
    salt = secrets.token_hex(10)
    salted_password = salt + updated_pass   
    hashed_password = hashlib.sha512(salted_password.encode()).hexdigest()

    if hashed_password == user.password:
        return Response({'message' : 'Cannot enter an old password'}, status=status.HTTP_400_BAD_REQUEST)
    
    Users.objects.filter(user_id=user.user_id).update(password=hashed_password, salt=salt)
    saved_otp.delete()
    
    sessionToken = Session.objects.get(user_id=user)
    sessionToken.delete()

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
        userser = UserSerializer(user)

        print('abl el try')

        try:

            #print("d5lt el try")
            
            #print(user)
            
            #print("cookie: " , request.COOKIES.get('token'))

            exist_token = Session.objects.get(user_id=user)

            #print("exist_token: " , exist_token)
            
            if exist_token.is_expired():
                exist_token.delete()
                print("expired token deleted")
            else:
                print("da5lt el else")
                sertoken = SessionSerializer(exist_token)
                response = Response({'message' : 'token already exists and redirect to home page' , "token": sertoken.data , "user":userser.data, "is_activated": user.is_activated})
                #response.set_cookie("token", exist_token.token)
                return response           
        except Session.DoesNotExist:
            pass
        except Session.MultipleObjectsReturned:
            print("da5lt el except")
            tokens = Session.objects.filter(user_id=user)
            tokens.delete()

        print("5alst el except")
        token  = Session.objects.create(user_id=user)
        token.generate_token()
        token.save()
        print("final token: " , token.token)
        tokenser = SessionSerializer(token)
        headers = {
        "Authorization":  token.token 
        }
        
        print("header: " , headers )
        response = Response({"message":"login successful", "token": tokenser.data, "user": userser.data, "is_activated": user.is_activated}  )#headers = headers
        #response.set_cookie('token', token.token) #expires=token.expires_at        
        print(" set cookies el fel 2wel login:  ", token.token)
        response["header"] = token.token
        
        return response
        
        
    else:
        return Response("incorrect password, please try again.")
    

@custom_auth_required
@api_view(['POST'])
def logout(request):
    
    data = getUser(request)
    user = data.data["user"]

    try:
        token = Session.objects.filter(user_id=user)
        token.delete()
    except Session.DoesNotExist:
        # redirect to login page
        pass

    return Response({'message : You are logged out'}, status=status.HTTP_200_OK)

@custom_auth_required
@api_view(['POST'])
def upload_pdf(request):
    message = ''
    
    data = getUser(request)
    user = data.data["user"]
    
    
    if not user.is_activated:
        return Response({'message' : 'User is not activated'}, status=status.HTTP_401_UNAUTHORIZED)
    

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
        document = Documents(user=user, document_name = pdf_file.name ,document_file=compressed_pdf, document_hash=pdf_hash, is_completed=False)
        document.save()
        
                
        if 'email_list' in request.data:
            list_of_gmail = request.data["email_list"] 
            for email in list_of_gmail:
                print("email: " , email)
                try:
                    party = Users.objects.get(email=email)
                    if not party.is_activated:
                        message += f'Email {party.email} is not active, '
                        continue
                except Users.DoesNotExist:
                    return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
                doc_shared = Document_shared(doc_id=document, owner_id = user, parties_id = party)
                try:
                    exist_ds = Document_shared.objects.filter(doc_id=document, owner_id = user, parties_id = party)
                    if exist_ds:
                        message += f'Email {party.email} was already added, '
                        continue
                except Document_shared.DoesNotExist:
                    pass
                doc_shared.save()
                subject = f'An invitation to a Contract from {user.email}'
                link = reverse('example', kwargs={"pk" : doc_shared.id, "user_id" : user.id})
                link_mssg = f'The user {user.firstname} {user.lastname} has offered you a contract in ehich you can review and accept or reject in the below link'
                recipient_list = [party.email]
                print("user.email: " , party.email)
                email = EmailMessage(subject, link_mssg, settings.EMAIL_HOST_USER, recipient_list)
                try:
                    email.send() 
                    message += f'Email sent to {party.email}'
                    # return Response({'message': f'Email sent to {party.email}'}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({'message' : 'emails were not provided'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'PDF uploaded and compressed successfully.' + message}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'PDF file not provided.'}, status=status.HTTP_400_BAD_REQUEST)


@custom_auth_required
@api_view(['POST'])
def email_add(request, doc_id):
    data = getUser(request)
    user = data.data["user"]

    message = ''

    try:
        document = Documents.objects.get(document_id=doc_id, user=user)
    except Documents.DoesNotExist:
        return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

    if 'email_list' in request.data:
        list_of_gmail = request.data["email_list"] 
        for email in list_of_gmail:
            print("email: " , email)
            try:
                party = Users.objects.get(email=email)
                if not party.is_activated:
                    message += f'Email {party.email} is not active, '
                    continue
            except Users.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            doc_shared = Document_shared(doc_id=document, owner_id = user, parties_id = party)
            try:
                exist_ds = Document_shared.objects.filter(doc_id=document, owner_id = user, parties_id = party)
                if exist_ds:
                    message += f'Email {party.email} was already added, '
                    continue
            except Document_shared.DoesNotExist:
                pass
            doc_shared.save()
            subject = f'An invitation to a Contract from {user.email}'
            # link = reverse('example', kwargs={"pk" : doc_shared.id, "user_id" : user.id})
            link = reverse('example', kwargs={"pk" : 3})
            full_link = settings.BASE_URL + link
            print("link:", link)
            link_mssg = f"The user {user.firstname} {user.lastname} has offered you a contract in which you can review and accept or reject in the below link <a href='{full_link}'>Click Here</a>"
            recipient_list = [party.email]
            print("user.email: " , party.email)
            email = EmailMessage(subject, link_mssg, settings.EMAIL_HOST_USER, recipient_list)
            email.content_subtype = "html"
            try:
                email.send() 
                message += f'Email sent to {party.email}'
                # return Response({'message': f'Email sent to {party.email}'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'Failed to send email: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message' : 'emails added'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'message' : 'emails not added'}, status=status.HTTP_400_BAD_REQUEST)

            
        

@api_view(['GET'])
@custom_auth_required
def get_document(request, pk):

    
    data = getUser(request)
    user = data.data["user"]
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

# still need to edit when using the BC
@api_view(['GET'])
@custom_auth_required
def get_document_details(request, pk):
    
    data = getUser(request)
    user = data.data["user"]
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



def example(request, pk):
    return render(request, 'users/example.html', {'title' : 'About'})

@api_view(['GET'])
def example_api(request):
    data = reverse('example', kwargs={"pk" : 3})
    return Response(data)
@api_view(['GET'])
@custom_auth_required
def documents_list(request):

    data = getUser(request)
    user = data.data["user"]

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

@api_view(['PUT'])
@custom_auth_required
def reject_document(request, doc_id):
    data = getUser(request)
    user = data.data["user"]
    try:
        docsh_id = Document_shared.objects.get(doc_id=doc_id, parties_id=user)
    except Document_shared.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    
    Document_shared.objects.filter(doc_id=doc_id, parties_id=user).update(is_accepted='rejected', time_a_r = timezone.now())
    return Response({'message' : 'Document rejected'}, status=status.HTTP_202_ACCEPTED)


@api_view(['PUT'])
@custom_auth_required
def confirm_document(request, doc_id):
    data = getUser(request)
    user = data.data["user"]
    try:
        doc = Document_shared.objects.get(doc_id = doc_id , parties_id=user)
    except Documents.DoesNotExist:
        return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    Document_shared.objects.filter(doc_id=doc_id, parties_id=user).update(is_accepted='accepted', time_a_r = timezone.now())
    
    return Response({'message': 'Document accepted'}, status=status.HTTP_200_OK)


def getUser(request):
    sessionToken = get_session_token(request)
    #ser = SessionSerializer(sessionToken)
    #print("sessionToken: " , sessionToken.token)
    try:
        print("d5lt el try")
        session = Session.objects.get(token=sessionToken.data)
        user = Users.objects.get(user_id=session.user_id_id)
        
        return Response({"user": user})
    except Session.DoesNotExist:
        return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    

# Change this to a normal method 
@custom_auth_required
@api_view(['GET'])
def get_confirmation(request, doc_id):
    data = getUser(request)
    user = data.data["user"]

    try:
        docs = Document_shared.objects.filter(doc_id = doc_id , owner_id=user)
    except Document_shared.DoesNotExist:
        try:
            documents = Documents.objects.get(document_id=doc_id, user=user)
        except Documents.DoesNotExist:
            return Response({'message': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)
        if documents:
            doc_ser = DocumentSerializer(documents)
            return Response({'message : Document is Acceepted. You are the only party', doc_ser.data}, status=status.HTTP_200_OK)
            
    
    accept = False
    for document in docs:
        if document.is_accepted == 'accepted':
            accept = True
        else:
            accept = False
            break
    
    if accept:
        acc_docs = DocumentSharedSerializer(docs, many=True)
        return Response({'message : All other parties have accepted', acc_docs.data}, status=status.HTTP_200_OK)
    
    r_docs = Document_shared.objects.filter(doc_id=doc_id, owner_id=user, is_accepted='rejected')
    rej_docs = DocumentSharedSerializer(r_docs, many=True)
    return Response({'message : Not all other parties have accepted', rej_docs.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@custom_auth_required
def get_all_shared(request, doc_id):
    data = getUser(request)
    user = data.data["user"]

    try:
        docs = Document_shared.objects.filter(doc_id = doc_id , owner_id=user)
        docs_ser = DocumentSharedSerializer(docs, many=True)
        return Response(docs_ser.data, status=status.HTTP_202_ACCEPTED)
    except Document_shared.DoesNotExist:
        return Response({'message' : 'You have not shared this document with any other user'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@custom_auth_required
def get_shared_with_user(request):
    data = getUser(request)
    user = data.data["user"]

    try:
        docs = Document_shared.objects.filter(parties_id=user)
        docs_ser = DocumentSharedSerializer(docs, many=True)
        return Response(docs_ser.data, status=status.HTTP_202_ACCEPTED)
    except Document_shared.DoesNotExist:
        return Response({'message' : 'You do not have any documents shared with you.'}, status=status.HTTP_404_NOT_FOUND)


def generate_url(request, tmeplate_name, attribute):
    url = reverse(tmeplate_name, kwargs={})
    print('url:',url)
    return f'<a href="{url}">Link Text</a>'