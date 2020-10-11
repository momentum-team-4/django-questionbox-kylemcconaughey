from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.db.models import Count, Min, F, Q
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer

# Create your views here.


def frontpage(request):
    questions = Question.objects.all().annotate(
        times_starred=Count("starred_by", distinct=True)
    )
    return render(request, "questionbox/frontpage.html", {"questions": questions})


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
        {"question": question, "answers": answers, "form": form},
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
