from django.db import models

class ChatEntry(models.Model):
    question = models.CharField(max_length=255, help_text="The user's question")
    answer = models.TextField(help_text="The corresponding answer")

    def __str__(self):
        return self.question
