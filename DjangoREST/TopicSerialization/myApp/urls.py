from django.urls import path
from .views import *

urlpatterns = [
    path('createUser/', user_create, name='user_create'),
]