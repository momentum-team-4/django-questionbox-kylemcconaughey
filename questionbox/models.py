from django.db import models
from users.models import User
from datetime import timedelta

# Create your models here.


class Question(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def niceCreated(self):
        nice_created = self.created_at - timedelta(hours=4)
        return nice_created.strftime("Created on %A at %I:%M %p")

    starred_by = models.ManyToManyField(
        to=User, related_name="starred_answer", blank=True
    )

    def __str__(self):
        return f"{self.title}"


class Answer(models.Model):
    body = models.TextField(null=False, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    starred_by = models.ManyToManyField(
        to=User, related_name="starred_answer", blank=True
    )

    def niceCreated(self):
        nice_created = self.created_at - timedelta(hours=4)
        return nice_created.strftime("Created on %A at %I:%M %p")
