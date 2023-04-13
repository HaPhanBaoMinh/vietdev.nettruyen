from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from comic.models import Comic
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from comic.models import Comic, Chap
# Create your models here.


class MyUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to='avatar/', default='avatar/default.jpg')
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username}"


class Follow(models.Model):
    unfollow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    readed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.comic}"


class BookMark(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    chap = models.ForeignKey(Chap, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    disabled = models.BooleanField(default=False)
