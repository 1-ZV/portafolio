import datetime, os
from django.db import models
from django.dispatch import receiver
from django.db.models.fields.files import ImageField
from django.db.models.signals import post_delete, pre_save
from django.db.models.fields import CharField, DateField, TextField



class Post(models.Model):
    title = CharField(max_length=100)
    description = TextField()
    image = ImageField(upload_to='blog/images')
    date = DateField(default=datetime.date.today)

@receiver(post_delete, sender=Post)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)

@receiver(pre_save, sender=Post)
def delete_pre_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        pre = Post.objects.get(pk=instance.pk)
    except Post.DoesNotExist:
        return

    if pre.image and pre.image != instance.image:
        pre.image.delete(save=False)