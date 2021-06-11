from django.http.response import HttpResponse
from django.views.generic import TemplateView

def helloworldfunction(request):
    returnobject = HttpResponse('Old HelloWorld!')
    return returnobject

class HelloWorldView(TemplateView):
    template_name = 'hello.html'