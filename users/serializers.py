from rest_framework.serializers import ModelSerializer , SerializerMethodField
from rest_framework import serializers
from .models import Users , Documents , Document_shared, OneTimePassword 


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
        
        


# class SessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Session
#         fields = ['user_id', 'token']