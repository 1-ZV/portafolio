from django.db import models
from django.dispatch import receiver
from django.db.models.fields import CharField, URLField
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_delete, pre_save

class Project(models.Model):
    title = CharField(max_length=100)
    description = CharField(max_length=100)
    image = ImageField(upload_to="portfolio/images/")
    url = URLField(blank=True)

@receiver(post_delete, sender=Project)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

@receiver(pre_save, sender=Project)
def delete_pre_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        pre = Project.objects.get(pk=instance.pk)
    except Project.DoesNotExist:
        return

    if pre.image and pre.image != instance.image:
        pre.image.delete(save=False)