from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blogs.sitemaps import PostSitemap

sitemaps = {
    "post": PostSitemap,
}

urlpatterns = [
    path('liberia/', admin.site.urls),
    path("",include('blogs.urls',namespace='blogs')),
    path('summernote/', include('django_summernote.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
