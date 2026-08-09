from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
        )
        extra_kwargs = {
            'password': {
                "write_only": True,    
            }   
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user
    
    def validate_email(self, value):
        return value.strip().lower()


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
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only = True,    
    )
    
    def validate(self, attrs):
        email=attrs.get("email"),
        password=attrs.get("password"),

        user = authenticate(
            email=email,
            password=password,
        )
        
        if user is None:
            raise serializers.ValidationError(
                "Invalid email or password"    
            )
        if not user.is_active:
            raise serializers.ValidationError(
                "This account is inactive."
            )
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),                
        }