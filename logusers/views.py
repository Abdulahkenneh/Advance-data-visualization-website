from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import CustomUserCreationForm,LoginForm
from blogs.models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    """View for user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('blogs:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'logusers/register.html', {'form': form})


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
    return render(request, 'logusers/login.html', {'form': form})


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect(reverse('blogs:home'))  # Redirect to the homepage after logout

