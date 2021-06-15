from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import TodoModel

# Create your views here.

class TodoList(ListView):
    template_name = 'list.html'
    model = TodoModel

class TodoDetail(DetailView):
    template_name = 'detail.html'
    model = TodoModel

class TodoCreate(CreateView):
    template_name = 'create.html'
    model = TodoModel
    fields = ('title','memo','priority','duedate')