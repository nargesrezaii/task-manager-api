from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.users.auth.serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserRegistrationSerializer,
)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        
        if not user.check_password(
            serializer.validated_data["old_password"]
        ):
            return Response(
                {"old_password":"Incorrect password."},
                status=400
            )
        user.set_password(
            serializer.validated_data["new_password"]    
        )
        user.save()
        
        return Response(
            {"detail": "Password changed successfully."}    
        )
    

class LoginView(APIView):
    permission_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )
        
        serializer.is_valid(raise_exception=True)
        
        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
        )
    

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Successfully logged out."})

    
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
            }
        )

