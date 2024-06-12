from django.urls import path
from .views import ide_view
from django.conf import settings
from django.conf.urls.static import static


app_name='python-ide'

urlpatterns =[
     path('',ide_view,name='ide'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
