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