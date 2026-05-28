from django.urls import path
from myApp.views import *

urlpatterns = [
    path('',home,name='home'),
    path('generate/',generate_form,name='generate_form'),
    path('result/',result_view,name='result'),
]