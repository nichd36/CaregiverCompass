from django.urls import path
from blog.views import(
    create_blog_view,
    detail_blog_view,
    edit_blog_view,
    quiz_view,
    quiz_data_view,
    save_quiz_view,
    bookmark_blog_view,
)

app_name = 'blog'

urlpatterns = [
    path('create/', create_blog_view, name="create"),
    path('<slug>/', detail_blog_view, name="detail"),
    path('<slug>/edit', edit_blog_view, name="edit"),
    path('<slug>/quiz', quiz_view, name="quiz"),
    path('<slug>/quiz/data', quiz_data_view, name="quiz-data"),
    path('<slug>/quiz/save', save_quiz_view, name="save-data"),
    path('<slug>/bookmark', bookmark_blog_view, name="bookmark-topic"),
]