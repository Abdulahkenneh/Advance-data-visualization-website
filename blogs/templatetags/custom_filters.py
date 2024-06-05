from django import template
import re
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='get_progress')
def get_progress(progress_dict, topic_id):
    return progress_dict.get(topic_id, None)

@register.filter(name='get_attr')
def get_attr(obj, attr):
    return getattr(obj, attr, None)

@register.filter(name='zip_lists')
def zip_lists(a, b):
    return zip(a, b)

@register.filter(name='as_bootstrap_radio')
def as_bootstrap_radio(field):
    return field.as_widget(attrs={'class': 'form-check-input'})


@register.filter
def truncate_words(value, num_words):
    """
    Truncate the given text after a given number of words.
    """
    words = re.findall(r'\w+', value)
    if len(words) > num_words:
        truncated_text = ' '.join(words[:num_words]) + '...'
    else:
        truncated_text = value
    return truncated_text