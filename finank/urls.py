from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# import test view from views.py
from .views import test, upload_receipt, expenses_overview, expenses_by_category

# create a path to the test view
urlpatterns = [
    path('test/', test, name='test'),
    path('upload-receipt/', upload_receipt, name='upload_receipt'),
    path('expenses-overview/', expenses_overview, name='expenses_overview'),
    path('expenses-by-category/', expenses_by_category, name='expenses_by_category'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)