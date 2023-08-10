from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from blog.models import BlogPost, Sessions
from preposttest.models import ResultPrePostTest
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from user.models import Account
from django.http import JsonResponse
from question.models import Question, Answer
from answer.models import Result
import math

def bookmark_blog_view(request, slug):
    topic = get_object_or_404(BlogPost, slug = request.POST.get('blog_post_slug'))
    bookmarked = False

    if topic.bookmarked.filter(email = request.user.email).exists(): 
        bookmarked = False
        topic.bookmarked.remove(request.user)
        print("\n\n\nFOUNDDDD\nRemoved from bookmark\n\n")
    else:
        bookmarked = True
        topic.bookmarked.add(request.user)
        print("\n\n\nNOT FOUND\nAdded to bookmark\n\n")

    return HttpResponseRedirect(reverse('blog:detail', kwargs={'slug': slug}))

def create_blog_view(request):
    context = {}
    user = request.user
    if not request.user.is_staff:
        return redirect('must_authenticate')
    
    form = CreateBlogPostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.save()
        form = CreateBlogPostForm()

    context['form'] = form

    return render(request, "blog/create.html", context)

def must_authenticate_view(request):
    return render(request, 'user/must_authenticate.html', {})

def detail_blog_view(request, slug):
    context = {}
    topic_selected = BlogPost.objects.get(slug=slug)
    section_content = topic_selected.session
    prev_result = 0.00

    topics = BlogPost.objects.filter(session = section_content).order_by('display_order')
    context['topics'] = topics

    if topic_selected == topics.first():
        print("\nYESS SAME\n")
        if request.user.is_authenticated:
            try:
                resultPretest = ResultPrePostTest.objects.get(pre_test__session=section_content, user=request.user, pre_test__test_type="pretest")
                prev_result = 100.00
            except ResultPrePostTest.DoesNotExist:
                prev_result = 0.00
                print("\nNOT FOUND, but 100\n")
        else:
            prev_result = 100.00
    else:
        for topic in topics:
            if topic == topic_selected :
                print("Title found:", topic_selected.title)
                break
            else:
                try:
                    if request.user.is_authenticated:
                        prev_result = Result.objects.get(user=request.user, quiz=topic).score
                    else: 
                        prev_result = 0.00
                except Result.DoesNotExist:
                    prev_result = 0.00

    print("Prev result:")
    print(prev_result)

    if prev_result != 100 and not request.user.is_authenticated:
        return redirect("topics")
    
    if prev_result != 100 and not request.user.is_admin:
        return redirect("topics")

    if request.is_ajax():
        print("request is_ajax")
        topic = request.POST.get('topicName')
        user = request.user
        return JsonResponse({'success': True})

    blog_post = get_object_or_404(BlogPost, slug=slug)
    total_likes = blog_post.get_bookmarked_count()

    bookmarked = False

    if request.user.is_authenticated:
        if blog_post.bookmarked.filter(email = request.user.email).exists(): 
            bookmarked = True

    wordCount = len(topic_selected.body.split())
    readingTime = wordCount/200

    context['reading_time'] = math.ceil(readingTime)
    context['bookmarked'] = bookmarked
    context['blog_post'] = blog_post
    context['total_likes'] = total_likes

    return render(request, 'blog/detail_blog.html', context)

def edit_blog_view(request, slug):
    user = request.user
    if not user.is_staff:
        return redirect('must_authenticate')
    
    context = {}

    blog_post = get_object_or_404(BlogPost, slug=slug)
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Topic updated"
            blog_post = obj
    
    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
            "image": blog_post.image,
        }
    )
    context['form'] = form
    return render(request, 'blog/edit_blog.html', context)

def quiz_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    quiz = BlogPost.objects.get(slug=slug)
    return render(request, 'blog/quiz.html', {'obj': quiz})

def quiz_data_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    quiz = BlogPost.objects.get(slug=slug)
    questions = []
    for q in quiz.get_questions():
        print(q)
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions, 
    })

def save_quiz_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    print(request.POST)
    if request.is_ajax() and not request.user.is_admin:
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        hasil = Result.objects.all()

        data_.pop('csrfmiddlewaretoken')
 
        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = BlogPost.objects.get(slug=slug)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier

        # if user = ser now
        # results.quiz.ttle = 

        email = request.user.email

        found = False

        for x in hasil:
            if x.user.email == email:
                if x.quiz.title == quiz.title:
                    found = True
                    if x.score < score_:
                        x.delete()
                        Result.objects.create(quiz=quiz, user=user,score=score_)
                        print(x.score)
                        print(score_)

        if found == False:
            Result.objects.create(quiz=quiz, user=user,score=score_)

        if score_ == 100 :
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

