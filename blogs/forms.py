# your_app/forms.py
from markitup.widgets import MarkItUpWidget
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Achievement
from django import forms
from .models import Question, Choice, UserAnswer,CourseTopic,Post,Comment,ContactUs,Subcribe,NewSubscribers
from tinymce.widgets import TinyMCE
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email
from django.contrib.auth import authenticate

#from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields= ['title','certificate']




class UserAnswerForm(forms.ModelForm):
    class Meta:
        model = UserAnswer
        fields = ['choice']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = question.choices.all()


class CourseTopicForm(forms.ModelForm):
    class Meta:
        model = CourseTopic
        fields = ['title', 'body', 'image','course']
     
      



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'thumbnail']
        widgets = {
            'body': MarkItUpWidget(attrs={'cols': 80, 'rows': 30}),
        }



class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name','email','message']
        


class SubcribeForm(forms.ModelForm):
    class Meta:
        model = Subcribe
        fields =['email']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title','message']

class NewsubcribersForm(forms.ModelForm):
    class Meta:
        model = NewSubscribers
        fields = ['email']