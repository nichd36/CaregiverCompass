# Generated by Django 4.2 on 2023-07-20 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('preposttest', '0006_rename_number_of_questions_pretest_number_of_mcq'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Answer',
            new_name='MultipleChoiceAnswer',
        ),
        migrations.RenameModel(
            old_name='QuestionAnswer',
            new_name='MultipleChoiceQuestionAnswer',
        ),
    ]
