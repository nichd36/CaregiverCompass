from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.core.mail import send_mail


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users need to have an username")
        
        user = self.model(
                email = self.normalize_email(email),
                username = username,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
                email = self.normalize_email(email),
                username = username,
                password = password,
            )
        
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email                       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                    = models.CharField(max_length=30, unique=False)
    date_joined                 = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login                  = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin                    = models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    image                       = models.ImageField(upload_to="images/", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    @receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
    def user_signed_up_(request, user, **kwargs):
        # user signed up now send email
        # send email part - do your self
        email = user.email
        subject = 'Welcome to DementiaLearn! 🎉 (Automated, do not reply)'
        message = 'Hi ' + user.username + ', we are delighted to meet you!\nWith open arms, we embrace you as a valued member of our community dedicated to understanding, supporting, and learning about dementia.\n\nBy joining our website, you have taken a significant step towards expanding your knowledge, gaining insights, and making a positive impact in the lives of those affected by dementia. We believe that education is a powerful tool, and together, we can create a more compassionate and informed society.\n\n\nTHIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL'
        from_email = 'your@example.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
        return
    
class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)