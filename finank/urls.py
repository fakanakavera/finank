from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import test view from views.py
from .views import test, upload_receipt

# create a path to the test view
urlpatterns = [
    path('test/', test, name='test'),
    path('upload-receipt/', upload_receipt, name='upload_receipt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)