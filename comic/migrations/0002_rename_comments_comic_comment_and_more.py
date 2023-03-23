# Generated by Django 4.1.7 on 2023-03-21 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comic',
            old_name='comments',
            new_name='comment',
        ),
        migrations.RenameField(
            model_name='comic',
            old_name='created',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comic',
            old_name='views',
            new_name='view',
        ),
        migrations.AlterField(
            model_name='comic',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('demale', 'female'), ('unisex', 'unisex')], default='unisex', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='comic',
            name='genres',
            field=models.ManyToManyField(to='comic.genre'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='image',
            field=models.ImageField(null=True, upload_to='comic/'),
        ),
        migrations.AlterField(
            model_name='comic',
            name='status',
            field=models.CharField(choices=[('updating', 'updating'), ('deleted', 'deleted'), ('ended', 'ended')], max_length=10, null=True),
        ),
    ]
