# Generated by Django 4.2 on 2023-07-20 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preposttest', '0009_rename_essay_essayanswer_test'),
    ]

    operations = [
        migrations.RenameField(
            model_name='essayanswer',
            old_name='test',
            new_name='question',
        ),
    ]