from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.db.models import Count, Min, F, Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer

# Create your views here.


def frontpage(request):
    questions = Question.objects.all().annotate(
        times_starred=Count("starred_by", distinct=True)
    )
    return render(
        request, "questionbox/frontpage.html", {"questions": reversed(questions)}
    )


def question_detail(request, pk):
    # what the question title href leads to

    questions = Question.objects.all().annotate(
        times_starred=Count("starred_by", distinct=True)
    )
    question = get_object_or_404(questions, pk=pk)
    answers = Answer.objects.filter(question=question).annotate(
        times_starred=Count("starred_by", distinct=True)
    )
    form = AnswerForm()
    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect(to="question_detail", pk=question.pk)
    return render(
        request,
        "questionbox/question_detail.html",
        {
            "question": question,
            "answers": reversed(answers),
            "form": form,
        },
    )


@login_required
def answer_create(request, pk):
    question = get_object_or_404(Question, pk=pk)

    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect(to="question_detail", pk=question.pk)
    return render(
        request,
        "questionbox/answer_create.html",
        {"form": form, "question": question},
    )


@login_required
def question_create(request):
    # Create a question to be asked
    if request.method == "GET":
        form = QuestionForm()

    else:
        form = QuestionForm(data=request.POST)

        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user

            temp.save()

            success(request, "Your question was asked!")
            return redirect(to="question_detail", pk=temp.pk)

    return render(request, "questionbox/question_create.html", {"form": form})


@login_required
def question_delete(request, pk):
    if request.method == "GET":
        return render(request, "questionbox/question_delete.html")
    else:
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        success(request, "Question has been deleted!")
        return redirect(to="frontpage")


@login_required
def answer_delete(request, pk):
    if request.method == "GET":
        return render(request, "questionbox/answer_delete.html")
    else:
        answer = get_object_or_404(Answer, pk=pk)
        answer.delete()
        success(request, "Answer has been delete!")
        return redirect(to="question_detail", pk=answer.question.pk)


@login_required
def homepage(request):
    # User profile page, should have all the things a registered user can do
    questions = Question.objects.filter(user=request.user).annotate(
        num_answers=Count("answers", distinct=True),
        times_starred=Count("starred_by", distint=True),
    )
    answers = Answer.objects.filter(author=request.user).annotate(
        times_starred=Count("starred_by", distinct=True)
    )
    starredQuestions = request.user.starred_questions.all()
    starredAnswers = request.user.starred_answers.all()
    return render(
        request,
        "questionbox/homepage.html",
        {
            "questions": questions,
            "answers": answers,
            "starredQuestions": starredQuestions,
            "starredAnswers": starredAnswers,
        },
    )


@csrf_exempt
@require_POST
def toggle_starred_question(request, question_pk):
    question = get_object_or_404(Question.objects.all(), pk=question_pk)

    if question in request.user.starred_questions.all():
        request.user.starred_questions.remove(question)
        return JsonResponse({"starred": False})

    request.user.starred_questions.add(question)
    return JsonResponse({"starred": True})


@csrf_exempt
@require_POST
def toggle_starred_answer(request, answer_pk):
    answer = get_object_or_404(Answer.objects.all(), pk=answer_pk)

    if answer in request.user.starred_answers.all():
        request.user.starred_answers.remove(answer)
        return JsonResponse({"starred": False})

    request.user.starred_answers.add(answer)
    return JsonResponse({"starred": True})


@csrf_exempt
@require_POST
def checkCorrect(request, answer_pk):
    answer = get_object_or_404(
        Answer.objects.filter(question__user=request.user), pk=answer_pk
    )

    if answer in request.user.correct_answers.all():
        request.user.correct_answers.remove(answer)
        return JsonResponse({"correct": False})

    request.user.correct_answers.add(answer)
    return JsonResponse({"correct": True})


def question_search(request):
    search_term = request.GET.get("q")
    if search_term:
        questions = Question.objects.filter(Q(title__icontains=search_term)).distinct()
    else:
        questions = None

    return render(
        request,
        "questionbox/search.html",
        {"questions": questions, "search_term": search_term},
    )
