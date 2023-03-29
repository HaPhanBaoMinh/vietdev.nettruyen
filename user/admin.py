from django.contrib import admin
from .models import MyUser, Follow, BookMark
# Register your models here.
# admin.site.register(MyUser)
# admin.site.register(Follow)


class MyUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_active")


admin.site.register(MyUser, MyUserAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'comic')


admin.site.register(Follow, FollowAdmin)


class BookMarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'comic', 'chap', 'disabled')


admin.site.register(BookMark, BookMarkAdmin)
 