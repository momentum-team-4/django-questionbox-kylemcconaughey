from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.db.models import Count, Min, F, Q
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, AnswerForm
from .models import Question, Answer

# Create your views here.


def frontpage(request):
    questions = Question.objects.all()
    return render(request, "questionbox/frontpage.html", {"questions": questions})


def question_detail(request, pk):
    # what the question title href leads to
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    form = AnswerForm()
    return render(
        request,
        "questionbox/question_detail.html",
        {"question": question, "answers": answers, "form": form},
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
    )
    answers = Answer.objects.filter(author=request.user)
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


@login_required
def answer_create(request, pk):
    # would love to have a textfield hidden that can be displayed on "click", whose contents are POSTed as the body of an answer that then gets displayed
    pass


@login_required
def submitted_by_user(request):
    # should have all the questions and answers submitted by user, set as links to said question/answer
    pass


@login_required
def starred_by_user(request):
    # Should have all the questions/answers that are starred by user
    pass