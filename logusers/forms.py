from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            try:
                validate_email(username)
            except ValidationError:
                raise forms.ValidationError("Enter a valid email address.")
        return username

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if '@' in username:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email address.")

        self.user_cache = authenticate(self.request, username=username, password=password)

        if self.user_cache is None:
            raise forms.ValidationError("Invalid login credentials.")

        return self.cleaned_data

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Enter a valid email address.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")

        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("The password must contain at least one digit.")

        if not any(char.isalpha() for char in password1):
            raise forms.ValidationError("The password must contain at least one letter.")

        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password1):
            raise forms.ValidationError("The password must contain at least one special character.")

        return password2
