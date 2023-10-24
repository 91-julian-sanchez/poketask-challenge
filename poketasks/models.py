from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    id = models.IntegerField(unique=True, primary_key=True)
    skills = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name