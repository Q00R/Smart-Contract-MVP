from django.shortcuts import render , redirect
from django.http import JsonResponse

from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Users , Documents ,Document_shared 

import secrets
import hashlib
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
            is_activated = True ,
            username = request.data['username'],
            nid = request.data['nid'],
            phone_number = request.data['phone number'],
            salt = salt
            )
        
        user.save()
        
        return Response('done')
        
    except:
        return Response('ERROR')
    




