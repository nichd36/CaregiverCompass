from django.db.models import Count
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import requests
from user.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, SocialAccountUpdateForm
from allauth.socialaccount.models import SocialAccount
from user.models import Account
from blog.models import BlogPost, Sessions
from preposttest.models import ResultPrePostTest
from answer.models import Result
from .models import Visitor
from django.conf import settings
from django.core.mail import send_mail
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.express as px
import io, math, os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import landscape
from PIL import Image
from django.templatetags.static import static
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from allauth.account.views import SignupView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone
from datetime import timedelta

def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)

            login(request, account)

            username = request.user.username
            subject = 'Welcome to DementiaLearn! 🎉 (Automated, do not reply)'
            message = 'Hi ' + username + ', we are delighted to meet you!\nWith open arms, we embrace you as a valued member of our community dedicated to understanding, supporting, and learning about dementia.\n\nBy joining our website, you have taken a significant step towards expanding your knowledge, gaining insights, and making a positive impact in the lives of those affected by dementia. We believe that education is a powerful tool, and together, we can create a more compassionate and informed society.\n\n\nTHIS IS AN AUTOMATED MESSAGE - PLEASE DO NOT REPLY DIRECTLY TO THIS EMAIL'
            email_from = settings.EMAIL_HOST_USER
            send_mail( subject, message, email_from, [email] )
            
            return redirect('home')
        else:
            context['registration_form'] = form
    else: #GET_request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'account/register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()
    
    context['login_form'] = form
    return render(request, 'account/login.html', context)

def account_view(request):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    else:
        allauth = SocialAccount.objects.filter(user=request.user).exists()
        print("\n\nALLAUTH:")
        print(allauth)

    context = {}
    if request.POST:
        if allauth:
            form = SocialAccountUpdateForm(request.POST, request.FILES,instance=request.user)

            if form.is_valid():
                form.initial = {
                    "username": request.POST['username'],
                }
                form.save()
                context['success_message'] = "Updated"
        else:
            form = AccountUpdateForm(request.POST, request.FILES,instance=request.user)
        
            if form.is_valid():
                form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
                }
                form.save()
                context['success_message'] = "Updated"
    else:
        if allauth:
            form = SocialAccountUpdateForm(initial={
            "username": request.user.username,
        })
        form = AccountUpdateForm(initial={
            "email": request.user.email, 
            "username": request.user.username,
        })

    context['account_form'] = form
    context['allauth'] = allauth
    
    return render(request, "account/account.html", context)

def detail_view(request):
    context = {}
    section_dict = []

    if not request.user.is_authenticated:
        return redirect('must_authenticate')

    user = request.user
    sections = Sessions.objects.all().order_by('display_order')
    result = Result.objects.filter(user = user)

    for section in sections:
        result_count = Result.objects.filter(quiz__session=section, user=user, score=100.00).count()
        topics_count = BlogPost.objects.filter(session=section).count()
        posttest_found = ResultPrePostTest.objects.filter(user=user, pre_test__session__title=section, pre_test__test_type="posttest")

        if topics_count > 0:
            process = (result_count / topics_count) * 100
        else:
            process = 0

        section_dict.append({
            'section': section,
            'process': process,
            'posttest_found': posttest_found
        })

    context['result'] = result
    context['user'] = user
    context['sections'] = section_dict
    return render(request, 'account/detail.html', context)

def reading_view(request):
    context = {}
    user = request.user

    if 'q' in request.GET:
        q = request.GET['q']
        bookmarks = BlogPost.objects.filter(bookmarked = user)
        bookmarks = bookmarks.filter(title__icontains=q)
    else:
        bookmarks = BlogPost.objects.filter(bookmarked=user)

    context ['bookmarks'] = []

    for bookmark in bookmarks:
        wordCount = len(bookmark.body.split())
        readingTime = math.ceil(wordCount/200)

        date_updated_str = bookmark.date_updated.strftime('%Y-%m-%d')
        
        post_data = {
        'title': bookmark.title,
        'slug': bookmark.slug,
        'date_updated': date_updated_str,
        'author': bookmark.author,
        'reading_time': readingTime,
    }
        context['bookmarks'].append(post_data)

    return render(request, 'account/reading.html', context)

def cert_pdf_view(request, title):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    else:
        # OLD CODE BASED ON QUIZ
        quiz_passed = 0
        result = Result.objects.filter(user = request.user, quiz__session__title = title)
        for r in result:
            if r.score == 100: quiz_passed=quiz_passed+1
        
        topics_count = BlogPost.objects.filter(session__title=title).count()
        process = quiz_passed/topics_count

        if process != 1: return redirect("topics")
        else:
            try:
                saved = ResultPrePostTest.objects.get(user=request.user, pre_test__session__title=title, pre_test__test_type="posttest")
            except ResultPrePostTest.DoesNotExist:
                return redirect ('topics')
    
    page_width, page_height = landscape((4*inch, 5.65*inch))
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(page_width, page_height), bottomup=0)
    
    center_x = page_width / 2
    
    username = request.user.username

    image_url = request.build_absolute_uri(static('cert.png'))
    response = requests.get(image_url)
    pil_img = Image.open(io.BytesIO(response.content))
    my_image = ImageReader(pil_img)

    img_width, img_height = my_image.getSize()

    x_scale = page_width / img_width
    y_scale = page_height / img_height
    scale = min(x_scale, y_scale)

    img_x = (page_width - img_width * scale) / 2
    img_y = (page_height - img_height * scale) / 2

    c.drawImage(my_image, img_x, img_y, width=img_width * scale, height=img_height * scale)

    c.setFont("Helvetica-Oblique", 30)
    c.drawString(center_x - (c.stringWidth(username, "Helvetica-Oblique", 30) / 2), 150, username)

    desc = "for completing the " + title
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.gray)
    c.drawString(center_x - (c.stringWidth(desc, "Helvetica", 11) / 2), 180, desc)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return the PDF as an attachment
    return FileResponse(buf, as_attachment=True, filename='certificate_'+ request.user.username +'.pdf')

def test_recaptcha_view(request):
    form = RegistrationForm()
    return render(request, 'account/test_recaptcha.html', {'form': form})



def statistic_view(request):
    qs = Account.objects.all()
    context = {}
    # Create a dictionary to store the count of users for each date
    user_count_by_date = {}

    for account in qs:
        date_joined = account.date_joined.date()  # Extract the date from the DateTimeField
        user_count_by_date[date_joined] = user_count_by_date.get(date_joined, 0) + 1

    # Sort the dictionary by date to maintain chronological order
    sorted_user_count = sorted(user_count_by_date.items(), key=lambda x: x[0])

    # Extract the dates and user counts as separate lists for plotting
    dates, user_counts = zip(*sorted_user_count)

    # Create the Plotly chart
    data = go.Scatter(x=dates, y=user_counts, mode='lines+markers', name='Number of Users')

    layout = go.Layout(
        xaxis_title='<b>Date</b>', 
        yaxis_title='Number of Users', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig_number_of_users = go.Figure(data=data, layout=layout)

    # Convert the Plotly figure to JSON
    plot_div_number_of_users = fig_number_of_users.to_json()

    total_number_of_users = Account.objects.all().count()

    a_week_ago = timezone.now() - timedelta(days=7)
    active_user_week = Account.objects.filter(last_login__gte=a_week_ago).count()

    completion_rate = {}
    sections = Sessions.objects.all().order_by('display_order')
    for section in sections:
        posttest_count = ResultPrePostTest.objects.filter(pre_test__session=section, pre_test__test_type="posttest").count()
        completion_rate[section] = round((posttest_count/total_number_of_users*100), 2)

    top_topics = BlogPost.objects.annotate(num_bookmarks=Count('bookmarked')).filter(num_bookmarks__gt=0).order_by('-num_bookmarks')[:3]

    visits = Visitor.objects.all()
    visits_count = visits.count()
    visitor_count_by_date = {}
    for visit in visits:
        date_visited = visit.timestamp  # Extract the date from the DateTimeField
        visitor_count_by_date[date_visited] = visitor_count_by_date.get(date_joined, 0) + 1

    sorted_visits = sorted(visitor_count_by_date.items(), key=lambda x: x[0])
    dates, visits = zip(*sorted_visits)
    visit_data = go.Scatter(x=dates, y=visits, mode='lines+markers', name='Number of Visits')

    visit_layout = go.Layout(
        xaxis_title='<b>Date</b>', 
        # xaxis_tickformat='%d',
        yaxis_title='Number of Visit(s)', 
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig_number_of_visits = go.Figure(data=visit_data, layout=visit_layout)
    plot_fig_number_of_visits = fig_number_of_visits.to_json()

    context['plot_div'] = plot_div_number_of_users
    context['plot_fig_number_of_visits'] = plot_fig_number_of_visits
    context['total_users'] = total_number_of_users
    context['active_user_week'] = active_user_week
    context['completion_rate'] = completion_rate
    context['top_topics'] = top_topics
    context['visits_count'] = visits_count

    return render(request, 'account/statistics.html', context)