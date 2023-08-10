from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from user.models import Account
import random

def upload_location(instance, filename):
    file_path = 'blog/{author_id}/{title}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path

class Sessions(models.Model):
    title                   = models.CharField(max_length=50, null=False, blank=False)
    body                    = models.CharField(max_length=5000, null=False, blank=False)
    image                   = models.ImageField(upload_to=upload_location, null=False, blank=False)
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    display_order           = models.IntegerField(blank=False, unique=True)

    def __str__(self):
        return self.title

    def get_blog(self):
        blog = self.blogpost_set.all().order_by('display_order')
        return blog

class BlogPost(models.Model):
    title                   = models.CharField(max_length=100, null=False, blank=False, unique=True)
    body                    = models.CharField(max_length=500000, null=False, blank=False)
    image                   = models.ImageField(upload_to=upload_location, null=False, blank=False)
    date_published          = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated            = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author                  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug                    = models.SlugField(blank=True, unique=True)
    number_of_questions     = models.IntegerField()
    session                 = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    bookmarked              = models.ManyToManyField(Account, related_name="topics", blank=True)
    display_order           = models.IntegerField(blank=False)

    def __str__(self):
        return self.title
    
    def get_questions(self):
        questions = list(self.question_set.all())
        random.shuffle(questions)
        return questions[:self.number_of_questions]
    
    def get_bookmarked_count(self):
        return self.bookmarked.count()
    
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

def pre_save_blog_post_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)

pre_save.connect(pre_save_blog_post_receiver, sender=BlogPost)