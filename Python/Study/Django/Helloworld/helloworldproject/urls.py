from django.conf.urls import include, url
from django.contrib import admin
from .views import HelloWorldView, helloworldfunction

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'hello/', include('helloworldapp.urls'))
]
