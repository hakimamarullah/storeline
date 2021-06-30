from django.shortcuts import render
from store.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
# Create your views here.
def accounts(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	address= CustomerAddress.objects.filter(customer=customer)
	cartItem = order.get_cart_items
	print(request.user.is_authenticated)
	context ={
		'user':customer,
		'cartItem': cartItem,
		'addresses': address
	}
	return render(request,'accounts/dashboard.html',context)

