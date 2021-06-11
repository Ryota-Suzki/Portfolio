from django.conf.urls import url
from .views import hellofunction

urlpatterns = [
    url(r'world/', hellofunction),
]
