from django.db import models
from blog.models import Sessions
from user.models import Account

# Create your models here.
class PreTest(models.Model):
    TEST_TYPES = (
        ('pretest', 'Pretest'),
        ('posttest', 'Posttest'),
    )

    test_type = models.CharField(choices=TEST_TYPES, max_length=10, default='pretest')
    # title                   = models.CharField(max_length=50, null=False, blank=False, unique=True)
    # body                    = models.CharField(max_length=5000, null=False, blank=False)
    date_published          = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated            = models.DateTimeField(auto_now=True, verbose_name="date updated")
    slug                    = models.SlugField(blank=True, unique=True)
    number_of_mcq           = models.IntegerField()
    session                 = models.ForeignKey(Sessions, on_delete=models.CASCADE, related_name='pretest')

    def __str__(self):
        return f"{self.test_type} - {self.session}"
    
    def get_questions(self):
        questions = list(self.multiplechoicequestion_set.all())
        return questions[:self.number_of_mcq]
    
    def get_essayquestions(self):
        essay_questions = list(self.essayquestion_set.all())
        return essay_questions
    
class MultipleChoiceQuestion(models.Model):
    text = models.CharField(max_length=200)
    test = models.ForeignKey(PreTest, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
    def get_answers(self):
        return self.multiplechoiceanswer_set.all()

class MultipleChoiceAnswer(models.Model):
    text = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text},  correct: {self.correct}"
    
class EssayQuestion(models.Model):
    text = models.CharField(max_length=200)
    test = models.ForeignKey(PreTest, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text)
    
class ResultPrePostTest(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    pre_test = models.ForeignKey(PreTest, on_delete=models.CASCADE)
    score = models.FloatField()
    answers = models.ManyToManyField(MultipleChoiceQuestion, through='MultipleChoiceQuestionAnswer')
    essayanswers = models.ManyToManyField(EssayQuestion, through='EssayAnswer')

class MultipleChoiceQuestionAnswer(models.Model):
    result = models.ForeignKey(ResultPrePostTest, on_delete=models.CASCADE)
    question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(MultipleChoiceAnswer, on_delete=models.CASCADE)

class EssayAnswer(models.Model):
    result = models.ForeignKey(ResultPrePostTest, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    question = models.ForeignKey(EssayQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.question}"
    
