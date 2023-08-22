from django.urls import path
from . import views



urlpatterns = [
    path('api/users/' , views.register),
    path('api/users/login/' ,views.login),
    path('api/users/documents/<str:pk>/' ,views.documents_list),
    path('api/users/<str:pk>/activate/' , views.activate),
    path('api/users/<str:pk>/verifyOTP/' , views.verify_otp),
    path('api/users/<str:pk>/deactivate/' , views.deactivate),
    path('api/users/<str:pk>/' ,views.EditAccount),
    path('api/users/<str:pk>/reset_password/' ,views.reset_password),
    path('api/documents/<str:pk>/upload/' ,views.upload_pdf),
    path('api/documents/<str:pk>/retrieve/' ,views.get_document),
    path('api/documents/<str:pk>/retrieve_details/' ,views.get_document_details),
    path('api/documents/<str:pk>/doclist/' ,views.documents_list),
    path('api/reject_document/<str:doc_id>/user/<str:user_id>' ,views.reject_document),
    path('api/confirm_document/<str:doc_id>/user/<str:user_id>' ,views.confirm_document),
]

