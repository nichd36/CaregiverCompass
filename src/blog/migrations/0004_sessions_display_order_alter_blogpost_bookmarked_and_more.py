# Generated by Django 4.2 on 2023-08-01 11:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0003_blogpost_bookmarked"),
    ]

    operations = [
        migrations.AddField(
            model_name="sessions",
            name="display_order",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="bookmarked",
            field=models.ManyToManyField(
                blank=True, related_name="topics", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="blogpost",
            name="title",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
