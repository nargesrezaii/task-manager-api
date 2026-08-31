from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from apps.tasks.models import Task

User = get_user_model()


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "priority",
            "due_date",
        )


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput    
    )
    

class RegistrationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput    
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput    
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )
        return email
    
    def clean_password(self):
        password = self.cleaned_data["password"]
        
        try:
            validate_password(password)
        except ValidationError as error:
            raise forms.ValidationError(error.messages)
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        
        if(
            password
            and password_confirm
            and password != password_confirm 
        ):
            raise forms.ValidationError(
                "Passwords do not match."
            )  
        
        return cleaned_data
    

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
        )
        

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Current password",
        widget=forms.PasswordInput,    
    )

    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,    
    )
    
    confirm_password = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput,    
    )


    def __init__(self, *args, user=None,**kwargs):
        super().__init__(*args, **kwargs)
        self.user=user


    def clean_current_password(self):
        password = self.cleaned_data["current_password"]
        
        if not self.user.check_password(password):
            raise forms.ValidationError(
                "Your current password is incorrect."    
            )
        
        return password


    def clean_new_password(self):
        password = self.cleaned_data["new_password"]

        validate_password(
            password,
            self.user,
        )
        
        return password
    

    def clean(self):
        cleaned_data = super().clean()
        
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if (
            new_password
            and confirm_password
            and new_password != confirm_password
        ):
            raise forms.ValidationError(
                "The new passwords do not match."    
            )
        
        return cleaned_data

