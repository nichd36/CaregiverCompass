"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
  re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
  re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

from personal.views import (
    home_screen_view,
    topics_view,
    success_view,
    error_view,
    contact_view,
    privacy_view,
    faq_view,
    about_view
)

from preposttest.views import(
    pretest_view,
)

from user.views import(
    registration_view,
    login_view,
    logout_view,
    account_view,
    must_authenticate_view,
    detail_view,
    reading_view,
    cert_pdf_view,
    statistic_view,
    test_recaptcha_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name="home"),
    path('about/', about_view, name='about'),
    path('blog/', include('blog.urls','blog')),
    path('preposttest/', include('preposttest.urls','preposttest')),    
    path('register/', registration_view, name="register"),
    path('logout/', logout_view, name="logout"),
    path('login/', login_view, name="login"),
    path('account/', account_view, name="account"),
    path('accounts/', include('allauth.urls')),
    path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('topics/', topics_view, name="topics"),
    path('detail/', detail_view, name='detail'),
    path('statistics/', statistic_view, name='statistics'),
    path('cert_pdf/<title>/', cert_pdf_view, name='cert_pdf'),
    path('reading/', reading_view, name='reading'),
    path('contact/', contact_view, name='contact'),
    path('faq/', faq_view, name='faq'),
    path('privacy/', privacy_view, name='privacy'),
    path('test-recaptcha/', test_recaptcha_view, name='test_recaptcha'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

    path("success/", success_view, name="success"),
    path("error/", error_view, name="error"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)