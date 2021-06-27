from django.shortcuts import render
from .models import *
import datetime
# Create your views here.
def store(request):
	product = Product.objects.all()
	context ={
		'products':product
	}
	return render(request,'store/store.html',context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		print(customer)
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		print(items)
	else:
		items=[]
	total_item = sum(item.quantity for item in items)
	total_harga = sum(item.product.price*item.quantity for item in items)

	context ={
		'items':items,
		'total_item':total_item,
		'total_harga':total_harga,
	}
	return render(request, 'store/cart.html',context)

def checkout(request):
	return render(request, 'store/checkout.html')
