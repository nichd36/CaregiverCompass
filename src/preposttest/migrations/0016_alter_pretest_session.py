# Generated by Django 4.2 on 2023-08-06 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_blogpost_body_alter_sessions_display_order'),
        ('preposttest', '0015_alter_pretest_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pretest',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pretest', to='blog.sessions'),
        ),
    ]