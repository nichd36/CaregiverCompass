from django.http import JsonResponse
from django.shortcuts import redirect, render
from blog.models import BlogPost
from answer.models import Result
from preposttest.models import PreTest, ResultPrePostTest
from preposttest.models import MultipleChoiceQuestion, MultipleChoiceAnswer, MultipleChoiceQuestionAnswer
from preposttest.models import EssayQuestion, EssayAnswer

# Create your views here.
def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})

def pretest_view(request, slug):
    quiz = PreTest.objects.get(slug=slug)

    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    elif not request.user.is_admin:
        try:
            saved = ResultPrePostTest.objects.get(user=request.user, pre_test=quiz)
            return redirect("topics")
        except ResultPrePostTest.DoesNotExist:
            print("No past result found.")

        print(quiz.test_type)
        if quiz.test_type == "posttest":
            quiz_passed = 0
            result = Result.objects.filter(user = request.user, quiz__session = quiz.session)
            for r in result:
                if r.score == 100: quiz_passed=quiz_passed+1
            
            topics_count = BlogPost.objects.filter(session=quiz.session).count()
            process = quiz_passed/topics_count

            if process != 1: return redirect("topics")
    
    return render(request, 'preposttest/pretest.html', {'obj': quiz})

def pretest_data_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    quiz = PreTest.objects.get(slug=slug)
    questions = []

    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    essay_questions = []
    for eq in quiz.get_essayquestions():
        print(eq)
        essay_questions.append(eq.text)

    return JsonResponse({
        'data': questions, 
        'essay_questions': essay_questions,
    })

def save_pretest_view(request, slug):
    if not request.user.is_authenticated:
        return redirect('must_authenticate')
    
    print(request.POST)
    if request.is_ajax() and not request.user.is_admin:
        questions = []
        essay_answers = []

        user = request.user
        quiz = PreTest.objects.get(slug=slug)

        data = request.POST
        data_ = dict(data.lists())

        data_.pop('csrfmiddlewaretoken')

        try:
            saved = ResultPrePostTest.objects.get(user=user, pre_test=quiz)
            print(saved.score)
            found = True
            print("\n\n\nFOUND OLD HISTORY\n\n\n")
            return JsonResponse({'passed': False})
        except ResultPrePostTest.DoesNotExist:
            print("No past result found.")
            found = False

        resultTemp = ResultPrePostTest.objects.create(pre_test=quiz, user=user, score=0)
        for key, value in data_.items():
            if key.startswith('essay_answer_'):
                q = key.replace('essay_answer_', '');
                question = EssayQuestion.objects.get(text=q)
                print(value)
                EssayAnswer.objects.create(result=resultTemp, question=question, user=user, answer_text=value)
            else:
                question = MultipleChoiceQuestion.objects.get(text=key)
                questions.append(question)
                # selected_answer = MultipleChoiceAnswer.objects.get(text=value)
 
        # for k in data_.keys():
        #     print('key: ', k)
        #     question = MultipleChoiceQuestion.objects.get(text=k)
        #     questions.append(question)
        # print(questions)
    
        score = 0
        multiplier = 100 / quiz.number_of_mcq
        results = []
        correct_answer = None

# issue cuz got a lot of answer, for now to check did dy or not rely on ResultPrePostTest
        # try:
        #     saved = EssayAnswer.objects.get(user=user, question=quiz)
        #     print("\n\n\nKETEMUUUUUUUU esai\n\n\n")
        #     found = True
        # except ResultPrePostTest.DoesNotExist:
        #     print("No past essay found.")
        #     found = False

        #create result first

        for q in questions:
            a_selected = request.POST.get(q.text)
            find_answer = MultipleChoiceAnswer.objects.filter(question=q)
            MultipleChoiceQuestionAnswer.objects.create(result=resultTemp, question=q, chosen_answer=find_answer.get(text = a_selected))
            
            if a_selected != "":
                question_answers = MultipleChoiceAnswer.objects.filter(question=q)

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
        score_ = round(score_, 2)

        try:
            if found == True:
                resultTemp.delete()
                print("delete resultTemp")

        except Exception as e:
            print(f"Error deleting object: {e}")

        
        resultTemp.score = score_
        resultTemp.save()
        return JsonResponse({'passed': True})
