from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from user_app.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"userlogininput"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"userlogininput"}))
    class Meta:
        model = User
        fields = ["username", "password"]
        

class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
        labels = {
            "first_name": "Имя"            
        }
        error_messages = {
            "username": {"unique":"Ты опоздал"}
        }