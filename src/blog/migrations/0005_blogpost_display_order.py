# Generated by Django 4.2 on 2023-08-01 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_sessions_display_order_alter_blogpost_bookmarked_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="display_order",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
