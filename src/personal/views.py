from django.http import HttpResponse
from django.shortcuts import render, redirect
from operator import attrgetter

from answer.models import Result
from preposttest.models import ResultPrePostTest
from user.models import Account
from blog.models import Sessions, BlogPost
from personal.models import Faq
from preposttest.models import PreTest

from django.shortcuts import redirect, render

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.conf import settings
from django.core.mail import send_mail

from django import template

import math

register = template.Library()

# Create your views here

api_key = "b92391bc4cb971e974c69df7794ff9f7-us21"
list_id = "c06a45ad70"
 
# function to manage subscriber
 
def success_view(request):
    return render(request, 'personal/success_newsletter.html')
 
def error_view(request):
    return render(request, 'personal/error_newsletter.html')

def topics_view(request):
    context = {}
    
    sections = Sessions.objects.all().order_by('display_order')
    section_topics_dict = {}
    temp_result = Result(score = 0.00)
        
    if request.user.is_authenticated == True:
        email = request.user.email
    else:
        email = ""

    if request.method=="POST":
        pick_section=request.POST.get('pick_section')
        result = Result.objects.filter(user__email__contains=email)
        context['result'] = result
    else :
        pick_section = Sessions.objects.order_by('display_order').first().title
        result = Result.objects.filter(user__email__contains=email)
        context['result'] = result

    section_info = {}    

    for section in sections:
        section_dict = {}
        section_dict['section'] = section
        section_dict['section_order'] = section.display_order

        section_dict['pretest'] = section.pretest.filter(test_type='pretest').first()
        section_dict['posttest'] = section.pretest.filter(test_type='posttest').first()

        
        quiz_passed = 0
        process = 0

        if request.user.is_authenticated:
            pretest_found = ResultPrePostTest.objects.filter(pre_test__session=section, user=request.user, pre_test__test_type="pretest").exists()
            posttest_found = ResultPrePostTest.objects.filter(pre_test__session=section, user=request.user, pre_test__test_type="posttest").exists()

            result = Result.objects.filter(user = request.user, quiz__session = section)
            for r in result:
                if r.score == 100: quiz_passed=quiz_passed+1
        else:
            pretest_found = False
            posttest_found = False
        
        if quiz_passed != 0:
            topics_count = BlogPost.objects.filter(session=section).count()
            process = (quiz_passed/topics_count)*100

        section_info[section] = process

        if process != 100:
            posttest_status = 1
        else:
            if posttest_found:
                posttest_status = 3
            else:
                posttest_status = 2

        section_dict['pretest_found'] = pretest_found
        section_dict['posttest_status'] = posttest_status

        blog_posts = section.get_blog()
        section_dict['blog_posts'] = []

        for index, blog_post in enumerate(blog_posts):
            previous_results = Result(score=0.00)
            
            if request.user.is_authenticated:
                result = Result.objects.filter(quiz=blog_post, user=request.user).first()
                if result is None:
                    result = Result(score=0.00)

                if index == 0:
                    try:
                        resultPretest = ResultPrePostTest.objects.get(pre_test__session=section, user=request.user, pre_test__test_type="pretest")
                        previous_results = Result(score=100.00)
                    except ResultPrePostTest.DoesNotExist:
                        previous_results = Result(score=0.00)
                        result = Result(score=0.00)
                else:
                    if temp_result is None:
                        previous_results = Result(score=0.00)
                    else:
                        previous_results = temp_result
            else:
                result = Result(score=0.00)
                if index == 0:
                    previous_results = Result(score=100.00)
                else:
                    previous_results = temp_result

            print("\n\nscore is")
            print(previous_results)

            
            wordCount = len(blog_post.body.split())
            readingTime = math.ceil(wordCount/200)

            section_dict['blog_posts'].append((blog_post, result.score if result else 0, previous_results, readingTime))
            
            temp_result = result

        section_topics_dict[section.title] = section_dict
    
    context['section_topics_dict'] = section_topics_dict

    # result_filtered = result.filter(quiz__session__title__contains=pick_section)
    # picked_section=Sessions.objects.filter(title__icontains = pick_section)

    topics = BlogPost.objects.filter(session__title = pick_section).order_by('display_order')

    context['section_info'] = section_info
    context['sections'] = sections
    context['topics'] = topics

    return render(request, "personal/topics.html", context)

def about_view(request):
    return render(request, 'personal/about.html')

def home_screen_view(request):
    context = {}

    sections = Sessions.objects.all()
    context['sections'] = sections

    if request.user.is_authenticated == True:
        username = request.user.username
        email = request.user.email
    else:
        username = ""
        email = ""

    context['username'] = username
    context['email'] = email

    if request.method == "POST":
        # getting users input from the form
        email = request.POST['email']
        username = request.POST['username']
 
        # initializing the mailchimp client with api key
        mailchimpClient = Client()
        mailchimpClient.set_config({
            "api_key": api_key,
        })
 
        userInfo = {
            "email_address": email,
            "status": "subscribed",
            "merge_fields": {
                "FNAME": username,
                "LNAME": "",
            }
        }
 
        try:
            # adding member to mailchimp audience list
            mailchimpClient.lists.add_list_member(list_id, userInfo)
            print("Success")
            
            # return HttpResponse('Subscribed Successfully')
            
        except ApiClientError as error:
            print(error.text)

            # return redirect("error")
        
    return render(request, 'personal/home.html', context)

def contact_view(request):
    if request.user.is_authenticated == True:
        username = request.user.username
        email = request.user.email
    else:
        username = ""
        email = ""

    context = {}
    context['username'] = username
    context['email'] = email

    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['name']
        content = request.POST['content']

        subject = 'Inquiry from ' + username
        message = 'An inquiry from\n' + username + ' ('+ email +')\n\n'+ content
        email_from = settings.EMAIL_HOST_USER
        send_mail( subject, message, email_from, [email_from] )
    return render(request, 'personal/contact.html', context)

def faq_view(request):
    if 'q' in request.GET:
        q = request.GET['q']
        faq = Faq.objects.filter(FAQquestion__icontains=q)
    else:
        faq = Faq.objects.all()
    context = {
        'faq': faq
    }
    return render(request, 'personal/faq.html', context)


def privacy_view(request):
    return render(request, 'personal/privacy.html')