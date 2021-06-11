from django.db import models

# Create your models here.

class TodoModel(models.Model):
    title = models.CharField(max_length=100)
    memo = models.TextField()
    def __str__(self): #string 特殊メソッド
        return self.title