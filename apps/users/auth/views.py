from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.auth.serializers import ChangePasswordSerializer


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