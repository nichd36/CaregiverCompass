from django.db import models
from blog.models import BlogPost
from user.models import Account
# Create your models here.

class Result(models.Model):
    quiz = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)

