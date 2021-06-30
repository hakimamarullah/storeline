from django.contrib import admin
from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('',views.store, name='store'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.processOrder, name='process-order'),
    path('view-product/<int:id>', views.viewProducts, name='view-product')
]