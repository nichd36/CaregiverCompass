from django.contrib import admin
from preposttest.models import PreTest, MultipleChoiceQuestion, MultipleChoiceAnswer, ResultPrePostTest, MultipleChoiceQuestionAnswer, EssayQuestion, EssayAnswer

# Register your models here.
admin.site.register(PreTest)

class AnswerInline(admin.TabularInline):
    model = MultipleChoiceAnswer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(MultipleChoiceQuestion, QuestionAdmin)
# admin.site.register(MultipleChoiceAnswer)
admin.site.register(ResultPrePostTest)
admin.site.register(MultipleChoiceQuestionAnswer)
admin.site.register(EssayAnswer)
admin.site.register(EssayQuestion)
