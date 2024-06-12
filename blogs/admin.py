# your_app/admin.py
from django.db import models
from tinymce.widgets import TinyMCE
from markitup.widgets import MarkItUpWidget
from django.contrib import admin
from .models import (Profile, Course,
                     Post, CourseTopic,Achievement,
                     UserCourseTopicProgress,Question,
                     UserAnswer,Choice,Comment,ContactUs,Subcribe
                     ,NewSubscribers,Items)

#from django_summernote.admin import SummernoteModelAdmin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'image']

@admin.register(NewSubscribers)
class NewSubcribersAdmin(admin.ModelAdmin):
    list_display = ['email']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'user']

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
   

admin.site.register(Post, PostAdmin)

@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},}
    list_display = ['owner','title', 'price','discription']
    


class CourseTopicAdmin(admin.ModelAdmin):
    list_display = [ 'title','body']
  

admin.site.register(CourseTopic, CourseTopicAdmin)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'certificate']

@admin.register(UserCourseTopicProgress)
class UserCourseTopicAdmin(admin.ModelAdmin):
    list_display = ['progress', 'user']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['question', 'text']


@admin.register(UserAnswer)
class UserCourseTopicAdmin(admin.ModelAdmin):
    list_display = ['question', 'user','choice']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']


@admin.register(Subcribe)
class SubcribeAdmin(admin.ModelAdmin):
    list_display = ['email']


@admin.register(Comment)
class ConmmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'message']



