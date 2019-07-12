from django.conf.urls import url

'''url(r'^rest-auth/tests/', include('rest_auth.tests.urls'))'''
urlpatterns = [


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)