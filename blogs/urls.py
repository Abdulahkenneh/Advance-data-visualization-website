from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, CourseTopicSitemap  # Import your sitemap classes
from .views import (
    home, recent_posts, course_topics, mark_topic_complete,
    register_course, all_courses, profile, course_delete_confirmation_view,
    unregister_course, my_courses, motivation_view, login_view, register,
    logout_view, quiz_results, take_quiz, add_course_topic, blogs_view,
    topics_view, download_achievement_view, share_achievement_view,
    create_blogpost, items_view
)

sitemaps = {
    'posts': PostSitemap,
    'topics': CourseTopicSitemap,
}

urlpatterns = [
    path('', home, name='home'),
    path('post/', blogs_view, name='post'),
    path('items/', items_view, name='items'),
    path('recent-posts/', recent_posts, name='recent_posts'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-topic/', add_course_topic, name='add_topic'),
    path('register_user/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('achievements/download/<int:id>/', download_achievement_view, name='download_achievement'),
    path('achievements/share/<int:id>/', share_achievement_view, name='share_achievement'),
    path('all_courses/', all_courses, name='all_courses'),
    path('my_courses/', my_courses, name='my_courses'),
    path('registers/<int:course_id>/', register_course, name='register_course'),
    path('topics/<int:topic_id>/', topics_view, name='topics'),
    path('motivation/<int:course_id>/', motivation_view, name='motivation'),
    path('course-topics/<int:course_id>/', course_topics, name='course_topics'),
    path('course-topics/complete/<int:topic_id>/', mark_topic_complete, name='mark_topic_complete'),
    path('unregister-course/<int:course_id>/', unregister_course, name='unregister_course'),
    path('confirm/<int:course_id>/', course_delete_confirmation_view, name='confirm'),
    path('course/<int:course_id>/quiz/', take_quiz, name='take_quiz'),
    path('course/<int:course_id>/quiz/results/', quiz_results, name='quiz_results'),
    path('entry/', create_blogpost, name='entry'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Include the following if statement for serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = 'blogs'
