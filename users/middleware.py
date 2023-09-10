from rest_framework import status
from functools import wraps
from django.http import JsonResponse
from users.models import Session
from rest_framework.response import Response

def custom_auth_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        session_response = get_session_token(request)
        print("session_response ely fel middl: " , session_response.data)
        
        if isinstance(session_response, Response):
            sessionToken = session_response.data
        else:
            return JsonResponse({"error": "sessionToken error"}, status=401)
        
        print("abo el so7ab sessionToken: " , sessionToken)
        try:
            userSession = Session.objects.get(token=sessionToken)
        except Session.DoesNotExist:
            return JsonResponse({"error": "user session not found"}, status=401)

        if  userSession.is_expired():
            userSession.delete()
            return JsonResponse({"error": "user session is expired"}, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def get_session_token(request):
    session_id = request.META.get("HTTP_SID")
    print("session_id fghjkl:", session_id)
    if session_id:
        try:
            session = Session.objects.get(token=session_id)

            print("deeh el session: " , session)
            
            return Response(session.token)
        except Session.DoesNotExist:
            return Response({'error': 'Session not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'No session token found'}, status=status.HTTP_404_NOT_FOUND)