from django.urls import path
from . import views


urlpatterns = [
    path('api/users/' , views.register),
    path('api/users/<str:pk>/activate/' , views.activate),
    path('api/users/<str:pk>/verifyOTP/' , views.verify_otp),
    path('api/users/<str:pk>/deactivate/' , views.deactivate),
    path('api/users/<str:pk>/' ,views.EditAccount )
]