# Generated by Django 4.1.7 on 2023-03-22 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0004_alter_comic_other_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='view_day',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comic',
            name='view_month',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comic',
            name='view_week',
            field=models.IntegerField(default=0),
        ),
    ]
