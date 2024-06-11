from django.urls import path

from .views import ide_view


app_name='python-ide'

urlpatterns =[
     path('',ide_view,name='ide'),
    
]