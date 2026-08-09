from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(
        self, 
        request,
        username=None,
        password=None,
        **kwargs,
    ):
        email=kwargs.get("email")
        if email is None:
            email = username
        
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        
        return None
    
    def get_user(self, user_id):
        try:
            return User.objcts.get(pk=user_id)
        except User.DoesNotExist:
            return None