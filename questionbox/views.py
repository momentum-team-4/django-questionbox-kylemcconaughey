from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import success, error
from django.db.models import Count, Min, F, Q
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *

# Create your views here.


def frontpage(request):
    # list of all questions asked by all users
    pass


@login_required
def homepage(request):
    # User profile page, should have all the things a registered user can do
    pass


@login_required
def question_create(request):
    # questionForm duh
    pass


def question_detail(request, pk):
    # what the question title href leads to
    pass


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