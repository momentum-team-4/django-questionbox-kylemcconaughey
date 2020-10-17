from django.db import models
from users.models import User
from datetime import timedelta

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)

    body = models.TextField(null=False, blank=False)

    asked_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="questions"
    )

    def niceAsked(self):
        nice_asked = self.asked_at - timedelta(hours=4)
        return nice_asked.strftime("%A, %b %d at %I:%M %p")

    starred_by = models.ManyToManyField(
        to=User, related_name="starred_questions", blank=True
    )

    def isStarred(self):
        if self.user in self.user.starred_questions.all():
            return True
        return False

    # either this or boolean on Answer
    # answered_by = models.OneToOneField(to=Answer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    body = models.TextField(null=False, blank=False)

    question = models.ForeignKey(
        to=Question, on_delete=models.CASCADE, related_name="answers"
    )

    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name="answers"
    )

    answered_at = models.DateTimeField(auto_now_add=True)

    starred_by = models.ManyToManyField(
        to=User, related_name="starred_answers", blank=True
    )

    correct = models.ManyToManyField(
        to=User, related_name="correct_answers", blank=True
    )

    def isCorrect(self):
        if self in self.question.user.correct_answers.all():
            return True
        return False

    def niceAnswered(self):
        nice_answered = self.answered_at - timedelta(hours=4)
        return nice_answered.strftime("%A, %b %d at %I:%M %p")

    def __str__(self):
        return f"{self.body}"
