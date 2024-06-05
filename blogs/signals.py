# myapp/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Achievement
from .utils import generate_certificate

@receiver(post_save, sender=Achievement)
def create_achievement_certificate(sender, instance, created, **kwargs):
    if created:
        generate_certificate(instance)
