from django.contrib import admin
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('accounts',views.accounts, name='accounts'),
    path('add-address/',views.addAddress, name='add-address'),
    path('del-address/<int:id>',views.deleteAddress, name='del-address'),
    path('edit-address/<int:id>',views.editAddress, name='edit-address'),
    path('login/',views.loginPage, name='login'),
    path('register/',views.register, name='register')
]