from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import test view from views.py
from .views import test

# create a path to the test view
urlpatterns = [
    path('test/', test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)