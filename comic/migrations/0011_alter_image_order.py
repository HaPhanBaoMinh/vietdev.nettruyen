# Generated by Django 4.1.7 on 2023-03-23 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0010_image_comic_alter_image_chap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='order',
            field=models.IntegerField(unique=True),
        ),
    ]