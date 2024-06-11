from django.contrib import admin
from .models import Integrated_development_env,CodeSnippet

# Register your models here.


@admin.register(Integrated_development_env)

class Integrated_development_envAdmin(admin.ModelAdmin):
    list_display = ['code']
    
    
    
@admin.register(CodeSnippet)
class CodeSnippetAdmin(admin.ModelAdmin):
    list_display = ['code']
