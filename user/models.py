from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from comic.models import Comic
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

class MyUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg')
    fullname = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.username} {self.is_active}"

class Follow(models.Model):
    unfollow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)   
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    readed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} {self.comic}"
 
@receiver(post_save, sender=Follow)
def update_follower_count(sender, instance, created, **kwargs):
    if created:
        comic = instance.comic
        comic.follower += 1
        comic.save()

@receiver(post_delete, sender=Follow)
def update_follower_count_on_delete(sender, instance, **kwargs):
    comic = instance.comic
    comic.follower -= 1
    comic.save()