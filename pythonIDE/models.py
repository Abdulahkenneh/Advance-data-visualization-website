from django.db import models

# Create your models here.


class Integrated_development_env(models.Model):
    code = models.TextField(blank=True,null=True)
    
    def __str__(self) -> str:
        return f'{self.code}'
    
    
class CodeSnippet(models.Model):
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.code}'
    
    
    
    

    