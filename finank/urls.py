from django.urls import path

# import test view from views.py
from .views import test

# create a path to the test view
urlpatterns = [
    path('test/', test, name='test'),
]