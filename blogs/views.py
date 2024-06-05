# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Course, CourseTopic, Profile,Achievement,UserCourseTopicProgress
from .forms import CustomUserCreationForm, ProfileForm,CommentForm,ContactForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm,AchievementForm
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, UserAnswer
from .forms import UserAnswerForm,CourseTopicForm,PostForm,SubcribeForm,NewsubcribersForm
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Course, Post, CourseTopic,Comment,Items
def home(request):
    items = Items.objects.all()
    courses = Course.objects.all()
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    topics = CourseTopic.objects.all()

    # Check if the request is for a specific post
    post_id = request.GET.get('post_id')

    if post_id:
        post = get_object_or_404(Post, id=post_id)
    else:
        post = page_obj.object_list[0] if page_obj.object_list else None

    contact_form = ContactForm(request.POST or None)

    if request.method == 'POST':
        if 'contact_submit' in request.POST and contact_form.is_valid():
            contact_form.save()
            return redirect('blogs:home')


    context = {
        'contact_form': contact_form,
        'courses': courses,
        'topics': topics,
        'page_obj': page_obj,
        'post': post,
        'items':items
    }
    return render(request, 'blogs/home.html', context)


def topics_view(request,topic_id):
    topics = CourseTopic.objects.all()
    topic = get_object_or_404(CourseTopic, id=topic_id)
    contex ={'topic':topic,'topics':topics}
    return  render(request,'blogs/topics.html',contex)


@login_required(login_url="/login/")
def blogs_view(request):
    items = Items.objects.all()
    courses = Course.objects.all()
    comments = Comment.objects.all()
    post_list = Post.objects.all().order_by('-created_at')  # Order by creation date, most recent first
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    topics = CourseTopic.objects.all()

    form = CommentForm()


    if request.method == 'POST':
        form = CommentForm(request.POST or None)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()

            return redirect('blogs:post')

    # Check if the request is for a specific post
    post_id = request.GET.get('post_id')
    if post_id:
        post = get_object_or_404(Post, id=post_id)
    else:
        post = page_obj.object_list[0] if page_obj.object_list else None

    return render(request, 'blogs/blogpost.html', {
        'courses': courses,
        'topics': topics,
        'page_obj': page_obj,
        'post': post,
        'form':form,
        'comments':comments,
        'items':items
    })


def all_courses(request):
    courses = Course.objects.all()
    return render(request, 'blogs/all_courses.html', {'courses': courses})


@login_required(login_url="/login/")
def my_courses(request):
    courses = Course.objects.filter(registered_users=request.user)

    # Calculate user-specific progress for each course
    user_course_progress = [
        {
            'course': course,
            'progress': course.overall_progress(request.user)
        }
        for course in courses
    ]

    return render(request, 'blogs/my_courses.html', {'user_course_progress': user_course_progress})


def recent_posts(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs/recent_posts.html', {'page_obj': page_obj})


@login_required(login_url="/login/")
def course_topics(request, course_id):
    course = get_object_or_404(Course, id=course_id, registered_users=request.user)
    topic_list = course.coursetopic_set.order_by('title')
    paginator = Paginator(topic_list, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_progress = UserCourseTopicProgress.objects.filter(user=request.user, topic__course_id=course_id)
    progress_dict = {up.topic_id: up for up in user_progress}

    # Check if all topics are completed
    all_completed = all(progress_dict.get(topic.id, UserCourseTopicProgress()).completed for topic in topic_list)

    certificate = None
    if all_completed:
        # Check if the user already has this achievement
        certificate, created = Achievement.objects.get_or_create(title=course.title, user=request.user)
        if created:
            certificate.save()

    return render(request, 'blogs/course_topics.html', {
        'course': course,
        'certificate': certificate,
        'page_obj': page_obj,
        'all_completed': all_completed,
        'progress_dict': progress_dict
    })


@login_required(login_url="/login/")
def mark_topic_complete(request, topic_id):
    topic = get_object_or_404(CourseTopic, id=topic_id)
    user_progress, created = UserCourseTopicProgress.objects.get_or_create(user=request.user, topic=topic)
    user_progress.completed = True
    user_progress.progress = 100
    user_progress.save()
    return redirect('blogs:course_topics', course_id=topic.course.id)



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('blogs:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'blogs/register.html', {'form': form})


@login_required(login_url="/login/")
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    achievements = Achievement.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('blogs:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ProfileForm(instance=user)

    mycourses = Course.objects.filter(registered_users=user)
    context = {
        'mycourses': mycourses,
        'form': form,
        'user': user,
        'achievements':achievements
    }
    return render(request, 'blogs/profile.html', context)


@login_required(login_url="/login/")
def download_achievement_view(request, id):
    achievement = get_object_or_404(Achievement, id=id)
    # Create response for file download
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{achievement.title}.pdf"'
    # Generate PDF content here (omitted for brevity)
    return response

@login_required(login_url="/login/")
def share_achievement_view(request, id):
    achievement = get_object_or_404(Achievement, id=id)
    # Implement share logic here (omitted for brevity)
    return redirect('blogs:profile')


@login_required(login_url="/login/")
def register_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user in course.registered_users.all():
        messages.warning(request, 'You are already registered for this course.')
    else:
        course.registered_users.add(request.user)
        messages.success(request, 'You have successfully registered for the course.')
    return redirect('blogs:my_courses')


@login_required(login_url="/login/")
def unregister_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user in course.registered_users.all():
        course.registered_users.remove(request.user)
        messages.success(request, 'You have successfully unregistered from the course.')
    else:
        messages.warning(request, 'You are not registered for this course.')
    return redirect('blogs:my_courses')


@login_required(login_url="/login/")
def course_delete_confirmation_view(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'blogs/confirm_course_deletion.html', context)

@login_required(login_url="/login/")
def motivation_view(request,course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'blogs/motivation.html',{'course':course})

# user section login,registration, and logout

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)  # Correct instantiation
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                return redirect('blogs:home')  # Redirect to the homepage after login
            else:
                form.add_error(None, 'Invalid email/username or password')
    else:
        form = LoginForm()
    return render(request, 'blogs/login.html', {'form': form})


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect(reverse('blogs:home'))  # Redirect to the homepage after logout



@login_required(login_url="/login/")
def take_quiz(request, course_id):
    questions = Question.objects.filter(course_id=course_id)
    course = get_object_or_404(Course,id=course_id)
    if request.method == 'POST':
        forms = []
        for question in questions:
            form = UserAnswerForm(request.POST, question=question)
            forms.append(form)
            if form.is_valid():
                user_answer, created = UserAnswer.objects.update_or_create(
                    user=request.user,
                    question=question,
                    defaults={'choice': form.cleaned_data['choice']}
                )
        return redirect('blogs:quiz_results', course_id=course_id)
    else:
        forms = [UserAnswerForm(question=question) for question in questions]
    return render(request, 'blogs/take_quiz.html', {'forms': forms,'course':course, 'questions': questions})

@login_required
def quiz_results(request, course_id):
    questions = Question.objects.filter(course_id=course_id)
    user_answers = UserAnswer.objects.filter(user=request.user, question__course_id=course_id)
    score = sum(1 for answer in user_answers if answer.choice.is_correct)
    total_questions = questions.count()
    return render(request, 'blogs/quiz_results.html', {
        'score': score,
        'total_questions': total_questions,
        'course_id':course_id
    })




@login_required(login_url="/login/")
def add_course_topic(request):
    if request.method == 'POST':
        form = CourseTopicForm(request.POST, request.FILES)
        if form.is_valid():
            course_topic = form.save(commit=False)
            course_topic.user = request.user  # Assign the logged-in user
            course_topic.save()
            return redirect('blogs:post')  # Replace with your view name
    else:
        form = CourseTopicForm()

    return render(request, 'blogs/add_course_topic.html', {'form': form})






def create_blogpost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()
            return redirect('blogs:post')  # Redirect after successful form submission
    else:
        form = PostForm()
    return render(request, 'blogs/create_blogpost.html', {'form': form})


    return render(request, 'blogs/base.html', {'form': form})



def items_view(request):
    items = Items.objects.all()
    return render(request,'blogs/items.html',{'items':items})