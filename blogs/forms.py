# your_app/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile,Achievement
from django import forms
from .models import Question, Choice, UserAnswer,CourseTopic,Post,Comment,ContactUs,Subcribe,NewSubscribers
from tinymce.widgets import TinyMCE
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm




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