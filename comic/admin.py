from django.contrib import admin
from .models import Genre, Comic, Chap, Image, Comment, Rating, Novels
# Register your models here.
# admin.site.register(Genre)
# admin.site.register(Image)
#  return f"{self.name} {self.view} {self.chap} {self.rating} {self.status}"


class ComicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "view", "chap", "rating",
                    "updated_at", "created_at", "status")


admin.site.register(Comic, ComicAdmin)


class ChapAdmin(admin.ModelAdmin):
    list_display = ("id", 'comic_id', "chap_num", "name", 'comic', 'is_novel')


admin.site.register(Chap, ChapAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ("order", "image", "chap_id", )


admin.site.register(Image, ImageAdmin)

class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


admin.site.register(Genre, GenreAdmin)


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('id', 'comic', 'user', 'content')


@admin.register(Rating)
class Rating(admin.ModelAdmin):
    list_display = ('comic', 'user', 'stars')


@admin.register(Novels)
class Novels(admin.ModelAdmin):
    list_display = ('chap', 'content')