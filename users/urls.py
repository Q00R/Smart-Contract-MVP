from django.urls import path
from . import views



urlpatterns = [
    path('api/users/' , views.register, name='register'),
    path('api/users/login/' ,views.log_in, name='login'),
    path('api/users/logout/' ,views.logout, name='logout'),
    path('api/users/documents/' ,views.documents_list, name='documents-list'),
    path('api/users/activate/' , views.activate, name='send-email-activate'),
    path('api/users/email_reset/' , views.email_pass_reset, name='send-pass-email-reset'), #send email for password reset
    path('api/users/verifyOTP/' , views.verify_otp, name='verify-email-otp'),
    path('api/users/deactivate/' , views.deactivate, name='deactivate'),
    path('api/users/Edit/' ,views.EditAccount, name='edit-account'),
    path('api/users/reset_password/' ,views.reset_password, name='reset-pass'), #reset password
    path('api/documents/upload/' ,views.upload_pdf, name='upload-doc'),
    path('api/documents/EmailAdd/<str:doc_id>/' ,views.email_add, name='add-emmail-to-doc'),
    path('review-share-doc/<int:pk>/', views.review_share_doc, name='review-share-doc'),
    path('api/example/', views.example_api),
    path('api/documents/<str:pk>/retrieve/' ,views.get_document, name='get-document'),
    path('api/documents/<str:pk>/retrieve_details/' ,views.get_document_details, name='get-document-details'),
    path('api/reject_document/<str:doc_id>/' ,views.reject_document, name='reject-docment'),
    path('api/confirm_document/<str:doc_id>/' ,views.confirm_document, name='accept-document'),
    path('api/confirmation/<str:doc_id>/' ,views.get_confirmation, name='get-confirmation'),
    path('api/get-shared/<str:doc_id>/' ,views.get_all_shared, name='get-shared'),
    path('api/get-shared-email/<str:doc_id>/' ,views.get_shared_email, name='get-shared-email'),
]

