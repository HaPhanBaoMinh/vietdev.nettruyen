from django.contrib import admin
from .models import Genre, Comic, Chap, Image, Comment, Rating
# Register your models here.
admin.site.register(Genre)
# admin.site.register(Chap)
#  return f"{self.name} {self.view} {self.chap} {self.rating} {self.status}"


class ComicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "view", "chap", "rating",
                    "updated_at", "created_at", "status")


admin.site.register(Comic, ComicAdmin)


class ChapAdmin(admin.ModelAdmin):
    list_display = ("chap_num", "name", "comic", "updated_at")


admin.site.register(Chap, ChapAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ("order", "image", "chap", "comic")


admin.site.register(Image, ImageAdmin)


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('comic', 'user', 'content')


@admin.register(Rating)
class Comment(admin.ModelAdmin):
    list_display = ('comic', 'user', 'stars')
