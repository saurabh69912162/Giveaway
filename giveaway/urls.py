from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url

urlpatterns = [
    path('creatosaurus-admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'', include('home.urls')),

]
