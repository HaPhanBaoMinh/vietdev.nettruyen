# Generated by Django 4.1.7 on 2023-03-28 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('comic', '0029_likecomment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likecomment',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='likecomment',
            name='like',
        ),
        migrations.AddField(
            model_name='likecomment',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='likecomment',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='like_cmt',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='likecomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]