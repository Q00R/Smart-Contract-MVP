from django.urls import path
from . import views


urlpatterns = [
    path('api/users/' , views.register),
    path('api/users/<str:pk>/activate/' , views.activate),
    path('api/users/verifyOTP/' , views.verify_otp)
]