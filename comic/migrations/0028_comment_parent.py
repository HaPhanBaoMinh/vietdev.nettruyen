# Generated by Django 4.1.7 on 2023-03-28 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0027_remove_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='comic.comment'),
        ),
    ]
