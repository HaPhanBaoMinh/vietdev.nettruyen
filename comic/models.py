import os
from django.utils import timezone

from django.db import models
# Create your models here.
from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Comic(models.Model):
    STATUS_CHOICES = (
        ("updating", "updating"),
        ("deleted", "deleted"),
        ("ended", "ended"),
    )
    GENDER_CHOICES = (
        ('male', "male"),
        ('female', 'female'),
        ('unisex', 'unisex')
    )

    name = models.CharField(max_length=255, null=False)
    other_name = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, null=True, default=None, blank=True)
    summary = models.CharField(max_length=1000, null=True, default=None)
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, null=True, default='unisex')
    image = models.ImageField(upload_to='comic/', null=True)
    rating = models.FloatField(default=0, null=False)
    follower = models.IntegerField(default=0, null=False)
    comment = models.IntegerField(default=0, null=False)
    chap = models.IntegerField(default=0, null=False)
    view = models.IntegerField(default=0, null=False)
    view_day = models.IntegerField(default=0, null=False)
    view_week = models.IntegerField(default=0, null=False)
    view_month = models.IntegerField(default=0, null=False)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return f"{self.name}"


class Chap(models.Model):
    chap_num = models.IntegerField(blank=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comic = models.ForeignKey(
        Comic, on_delete=models.CASCADE, related_name="chapter")

    def __str__(self):
        return f"{self.id} - {self.name} - {self.comic}"


@receiver(post_save, sender=Chap)
def update_chapter_count(sender, instance, created, **kwargs):
    if created:
        comic = instance.comic
        comic.chap += 1
        comic.save()
        
        # Create folder to store image
        folder_name = "comic_{0}_chapnum_{1}".format(comic.id, instance.chap_num)
        path = "{}/chap/{}".format(settings.MEDIA_ROOT, folder_name)
        if os.path.exists(path): return
        
        try:
            os.mkdir(path)
        except OSError as error:
            print(error)


@receiver(post_delete, sender=Chap)
def update_chapter_count_on_delete(sender, instance, **kwargs):
    comic = instance.comic
    comic.chap -= 1
    comic.save()

    # Delete folder store image when delete Chap 
    folder_name = "comic_{0}_chapnum_{1}".format(comic.id, instance.chap_num)
    path = "{}/chap/{}".format(settings.MEDIA_ROOT, folder_name)
    if not os.path.exists(path): return
    try:
        os.rmdir(path)
    except OSError as error:
        print(error)

def get_image_upload_path(instance, filename):
    comic_id = instance.chap.comic.id
    chap_num = instance.chap.chap_num
    folder_name = "comic_{0}_chapnum_{1}".format(comic_id, chap_num)
    return os.path.join("chap", folder_name, filename)
class Image(models.Model):
    image = models.ImageField(upload_to=get_image_upload_path)
    order = models.IntegerField()
    chap = models.ForeignKey(
        Chap, on_delete=models.CASCADE, related_name="chap")

    def __str__(self):
        return f"{self.order} {self.image}  {self.chap.name}"
        

    # Save image to corect folder 
    def save(self, *args, **kwargs):
        folder_name = "comic_{0}_chapnum_{1}".format(self.chap.comic.id, self.chap.chap_num)
        folder_path = os.path.join(settings.MEDIA_ROOT, 'chap', folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.image.upload_to = folder_name
        file_ext = os.path.splitext(self.image.name)[1]
        self.image.name = 'order_{0}{1}'.format(self.order, file_ext)
        super().save(*args, **kwargs)

@receiver(post_delete, sender=Image)
def delete_imageFile_on_delete(sender, instance, **kwargs):
    chap = instance.chap
    comic = chap.comic
    chap_num = chap.chap_num

    # Delete image file
    folder_name = "comic_{0}_chapnum_{1}".format(comic.id, chap_num)
    image_name = "order_{0}{1}".format(instance.order, os.path.splitext(instance.image.name)[1])
    path = os.path.join(settings.MEDIA_ROOT, 'chap', folder_name, image_name)
    if os.path.exists(path):
        os.remove(path)

