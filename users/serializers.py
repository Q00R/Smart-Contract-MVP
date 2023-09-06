from rest_framework.serializers import ModelSerializer , SerializerMethodField
from rest_framework import serializers
from .models import Users , Documents , Document_shared, OneTimePassword 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id' , 'firstname' , 'lastname' , 'email' , 'nid' , 'phone_number']
        
        
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'
        
        
class DocumentSharedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_shared
        fields = '__all__'

class OneTimePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneTimePassword
        fields = '__all__'
        

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['firstname'] = user.firstname
        token['lastname'] = user.lastname
        token['email'] = user.email
        token['nid'] = user.nid
        token['phone_number'] = user.phone_number
        token['is_active'] = user.is_active
        # ...

        return token


# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Session
#         fields = ['user_id', 'token']