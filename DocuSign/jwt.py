from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.settings import api_settings

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        try:
            raw_token = self.get_raw_token(request)
            validated_token = self.get_validated_token(raw_token)
            user = self.get_user(validated_token)
            # Your custom authentication logic here
            return user, validated_token
        except InvalidToken:
            pass

api_settings.AUTHENTICATION_CLASSES = [CustomJWTAuthentication]
