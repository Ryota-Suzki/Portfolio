from django.urls import path
from .views import TodoList , TodoDetail

urlpatterns = [
    path('list/', TodoList.as_view()),
    path('detail/<int:pk>', TodoDetail.as_view())
]
