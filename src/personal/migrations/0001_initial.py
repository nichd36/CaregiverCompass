# Generated by Django 4.2 on 2023-07-19 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FAQquestion', models.TextField()),
                ('FAQanswer', models.TextField()),
            ],
        ),
    ]
