# Generated by Django 4.1.7 on 2023-03-21 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0002_rename_comments_comic_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
