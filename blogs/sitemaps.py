from django.contrib.sitemaps import Sitemap
from .models import Post,CourseTopic
from django.urls import reverse


class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Post.objects.all()

    def lastmod(self, obj):
        return obj.created_at  # Assuming you have an 'updated_at' field in your Post model

class CourseTopicSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return CourseTopic.objects.all()

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return reverse('blogs:topics', kwargs={'topic_id': obj.id})










# class PostSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.8
#
#     def items(self):
#         return Post.objects.all()
#     def lastmod(self, obj):
#         return obj.created_at
#
#     def location(self, obj):
#         return obj.get_absolute_url()
#
# class StaticViewSitemap(Sitemap):
#     def items(self):
#         return ['blogs:home','blogs:post','blogs:all_courses','blogs:items']
#
#     def location(self, item):
#         return reverse(item)
