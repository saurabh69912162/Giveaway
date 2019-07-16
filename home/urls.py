"""giveaway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from home.views import *
from django.contrib import admin
from django.urls import path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import User

urlpatterns = [
    path('', views.default, name='default'),
    url(r'^cr-admin/',views.adminonly),
    url(r'^youtube-comment-frequency/$',views.comment_frequency),
    url(r'^youtube-comments-winner/(?P<giveaway_id>[\w|\W]+)/$',views.ytcomments, name='ytcommentwinner'),
    url(r'^announce-winner/',views.announce_winner),
    path('home/', views.profile, name='home'),
    url(r'^winner/$', views.winner, name='winner'),
    #url(r'^(?P<user>[-\w|\W]+)/end-giveaway/(?P<giveaway_id>[\w|\W]+)/winner/$', views.winner, name='winner'),
    url(r'^(?P<user>[-\w|\W]+)/(?P<giveaway_id>[\w|\W]+)/add_or_modify_rules/$', views.add_modify_rules, name='add_modify_rules'),
    url(r'^(?P<user>[-\w|\W]+)/end-giveaway/(?P<giveaway_id>[\w|\W]+)/$', views.endpage, name='endpage'),
    url(r'^(?P<user>[-\w|\W]+)/(?P<giveaway_id>[\w|\W]+)/$', views.detailpage, name='detailpage'),
    url(r'^(?P<user>[-\w|\W]+)/$', views.user, name='user'),



]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


