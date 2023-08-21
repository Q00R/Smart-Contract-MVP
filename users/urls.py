from django.urls import path
from . import views



urlpatterns = [
    path('api/users/' , views.register),
    path('api/users/login/' ,views.login),
    path('api/users/<str:pk>/activate/' , views.activate),
    path('api/users/<str:pk>/verifyOTP/' , views.verify_otp),
    path('api/users/<str:pk>/deactivate/' , views.deactivate),
    path('api/users/<str:pk>/' ,views.EditAccount),
    path('api/users/<str:pk>/reset_password/' ,views.reset_password),
    path('api/users/<str:pk>/upload/' ,views.upload_pdf),
    path('api/example/', views.example_api),
]