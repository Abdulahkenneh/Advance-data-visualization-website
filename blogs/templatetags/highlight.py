from django import template
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import re

register = template.Library()

@register.filter(name='syntax_highlight')
def syntax_highlight(content):
    formatter = HtmlFormatter()
    def replacer(match):
        code = match.group(1)
        lexer = get_lexer_by_name('python')  # Assuming the default language is Python; modify as needed
        return highlight(code, lexer, formatter)
    
    pattern = re.compile(r'```(.*?)```', re.DOTALL)
    return pattern.sub(replacer, content)