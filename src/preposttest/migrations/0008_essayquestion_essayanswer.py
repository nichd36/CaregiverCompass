# Generated by Django 4.2 on 2023-07-20 05:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('preposttest', '0007_rename_answer_multiplechoiceanswer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EssayQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preposttest.pretest')),
            ],
        ),
        migrations.CreateModel(
            name='EssayAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('essay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='preposttest.essayquestion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
