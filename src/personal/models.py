from django.db import models

class Faq(models.Model):
    FAQquestion             = models.TextField()
    FAQanswer               = models.TextField()

    def __str__(self):
        return self.FAQquestion

def upload_location(instance, filename):
    file_path = 'staff/{name}-{filename}'.format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path

class Staff(models.Model):
    name                    = models.TextField(blank=False)
    image                   = models.ImageField(upload_to=upload_location, null=False, blank=False)
    education               = models.TextField(blank=False)
    title                   = models.TextField(blank=False)
    phone                   = models.TextField()
    email                   = models.TextField()
    detail                  = models.TextField(blank=False)



    