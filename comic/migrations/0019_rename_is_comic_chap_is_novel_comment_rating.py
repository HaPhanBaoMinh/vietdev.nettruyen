# Generated by Django 4.1.7 on 2023-04-13 08:39

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comic', '0018_chap_is_comic_comment_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chap',
            old_name='is_comic',
            new_name='is_novel',
        ),

    ]
