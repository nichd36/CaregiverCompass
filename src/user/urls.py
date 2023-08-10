from django.urls import path
from user.views import test_recaptcha_view
from blog.views import(
    bookmark_view
)

app_name = 'account'

urlpatterns = [
    path('bookmark/', bookmark_view, name="bookmark"),
]