# Generated by Django 4.1.7 on 2023-04-06 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comic', '0037_comment_likes_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='chap',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='comic.chap'),
        ),
    ]