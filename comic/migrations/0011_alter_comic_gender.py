# Generated by Django 4.1.7 on 2023-03-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0010_rename_sumary_comic_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('unisex', 'unisex')], default='unisex', max_length=10, null=True),
        ),
    ]