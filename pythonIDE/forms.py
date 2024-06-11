from django import forms
from .models import Integrated_development_env

from .models import CodeSnippet

class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['code']
        

class IDE_form(forms.ModelForm):
    class Meta:
        model = Integrated_development_env
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'id': 'code'}),    
            
        }
        
                       
    
