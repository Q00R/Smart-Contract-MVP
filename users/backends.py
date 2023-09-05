from django.contrib.auth.backends import BaseBackend
from .models import Users
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

class CustomJWTAuthentication(JWTAuthentication):
    def custom_user_authentication_rule(self, validated_token):
        User = get_user_model()
        try:
            user_id = validated_token['id']
            user = User.objects.get(id=user_id)
        except (User.DoesNotExist, KeyError):
            return None
        # Return the user even if they are not active
        return user


class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Users.objects.get(email=email)
            if user.check_password(password):
                return user
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
        

