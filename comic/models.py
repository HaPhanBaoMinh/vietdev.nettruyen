from django.utils import timezone

from django.db import models
# Create your models here.
from django.apps import apps
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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
    author = models.CharField(max_length=255, null=True, default=None)
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
        return f"{self.id} {self.name} {self.view} {self.chap} {self.rating} {self.updated_at} {self.created_at} {self.status}"


class Chap(models.Model):
    chap_num = models.IntegerField(blank=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comic = models.ForeignKey(
        Comic, on_delete=models.CASCADE, related_name="chapter")

    def __str__(self):
        return f"{self.chap_num} {self.name} {self.comic.name} {self.updated_at}"


@receiver(post_save, sender=Chap)
def update_chapter_count(sender, instance, created, **kwargs):
    if created:
        comic = instance.comic
        comic.chap += 1
        comic.save()


@receiver(post_delete, sender=Chap)
def update_chapter_count_on_delete(sender, instance, **kwargs):
    comic = instance.comic
    comic.chap -= 1
    comic.save()


class Image(models.Model):
    image = models.ImageField(upload_to='chap/')
    order = models.IntegerField()
    chap = models.ForeignKey(
        Chap, on_delete=models.CASCADE, related_name="chap")

    def __str__(self):
        return f"{self.order} {self.image}  {self.chap.name} "
