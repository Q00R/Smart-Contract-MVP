from rest_framework.serializers import ModelSerializer , SerializerMethodField
from rest_framework import serializers
from .models import Users , Documents , Document_shared, OneTimePassword


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
        
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