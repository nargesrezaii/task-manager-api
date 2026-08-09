from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only = True    
    )
    new_password = serializers.CharField(
        write_only = True,
        validators=[validate_password],
    )
    new_password_confirmation = serializers.CharField(
        write_only = True    
    )
    
    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirmation"]:
            raise serializers.ValidationError(
                 {
                    "new_password_confirmation": (
                        "Passwords do not match."
                    )
                }  
            )
        return attrs