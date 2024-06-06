from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid



class Course(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_courses')
    registered_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='registered_courses', blank=True)

    def __str__(self):
        return self.title

    def is_complete(self, user):
        return all(
            UserCourseTopicProgress.objects.filter(user=user, topic=topic).first().completed
            for topic in self.coursetopic_set.all()
        )

    def overall_progress(self, user):
        topics = self.coursetopic_set.all()
        if not topics:
            return 0
        user_progress = UserCourseTopicProgress.objects.filter(user=user, topic__course=self)
        if not user_progress:
            return 0
        total_progress = sum(up.progress for up in user_progress)
        return total_progress / topics.count()



class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='images', blank=True)

    def get_absolute_url(self):
        return reverse('blogs:post')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class CourseTopic(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)
    progress = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('topics', kwargs={'topic_id': self.id})
    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, blank=True)
    lastname = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)
    bio = models.TextField(blank=True)
    enroll_courses = models.ManyToManyField('Course', related_name='students', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

class Achievement(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title =models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    certificate = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)

    def __str__(self):
        return f'{self.user},obtained {self.title} certificate on{self.date}'


#compiler


class UserCourseTopicProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(CourseTopic, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'topic')

    def __str__(self):
        return f"{self.user.username} - {self.topic.title}"


class Question(models.Model):
    text = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class UserAnswer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'question')



class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=False)
    message = models.TextField(blank=True,null= True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} send you {self.message} on {self.date}'





class Subcribe(models.Model):
    email = models.EmailField(blank=False,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} has subcribe on {self.date}'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True,null=True)
    message = models.TextField(blank=False,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.message}'


class NewSubscribers(models.Model):
    email = models.EmailField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.email} subscrbe on {self.date}'


class Items(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200,blank=True,null=True)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, blank=True)
    discription = models.TextField(blank=False,null=True)
    price = models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} the price is {self.price}'