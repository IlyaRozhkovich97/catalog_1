from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, Version

@receiver(post_save, sender=Product)
def create_initial_version(sender, instance, created, **kwargs):
    if created:
        Version.objects.create(
            product=instance,
            version_number='1.0',
            version_name='Initial Release',
            is_current=True
        )