from django.contrib import admin
from django.urls import path
from . import views

app = 'store'

urlpatterns = [
    path('',views.index, name='index'),
]