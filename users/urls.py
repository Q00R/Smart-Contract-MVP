from django.urls import path
from . import views



urlpatterns = [
    path('api/users/' , views.register),
    path('api/users/login/' ,views.login),
    path('api/users/logout/' ,views.logout),
    path('api/users/documents/' ,views.documents_list),
    path('api/users/activate/' , views.activate),
    path('api/users/email_reset/' , views.email_pass_reset),
    path('api/users/verifyOTP/' , views.verify_otp),
    path('api/users/deactivate/' , views.deactivate),
    path('api/users/Edit/' ,views.EditAccount),
    path('api/users/reset_password/' ,views.reset_password),
    path('api/documents/upload/' ,views.upload_pdf),
    path('api/documents/EmailAdd/<str:doc_id>/' ,views.email_add),
    path('review-share-doc/<int:pk>/', views.review_share_doc, name='review-share-doc'),
    path('api/example/', views.example_api),
    path('api/documents/<str:pk>/retrieve/' ,views.get_document),
    path('api/documents/<str:pk>/retrieve_details/' ,views.get_document_details),
    path('api/reject_document/<str:doc_id>/' ,views.reject_document),
    path('api/confirm_document/<str:doc_id>/' ,views.confirm_document),
    path('api/confirmation/<str:doc_id>/' ,views.get_confirmation),
]

