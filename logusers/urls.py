from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import login_view, register,logout_view

urlpatterns = [
     path('register_user/', register, name='register'),
     path('login/',login_view,name = 'login'),
     path('logout/',logout_view,name='logout')
]

app_name = 'logusers'
