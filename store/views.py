from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
# Create your views here.
def store(request):
	product = Product.objects.all()
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItem = order.get_cart_items
	else:
		items=[]
		order={'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		cartItem = order['get_cart_items']
	context ={
		'products':product,
		'cartItem': cartItem
	}
	return render(request,'store/store.html',context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItem = order.get_cart_items
	else:
		items=[]
		order={'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		cartItem = order['get_cart_items']
	context ={
		'items':items,
		'orders': order,
		'cartItem': cartItem
	}
	return render(request, 'store/cart.html',context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItem = order.get_cart_items
		address = CustomerAddress.objects.filter(customer=customer, is_default=True)
	else:
		items=[]
		address = []
		order={'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
		cartItem = order['get_cart_items']
	context ={
		'items':items,
		'orders': order,
		'cartItem': cartItem,
		'address': address
	}
	return render(request, 'store/checkout.html',context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, create = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity += 1
	elif action == 'remove':
		orderItem.quantity -=1
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse("Item added", safe=False)

def processOrder(request):
	data = json.loads(request.body)
	
	if request.user.is_authenticated:
		customer = request.user.customer
		transaction_id = datetime.datetime.now().timestamp()
		order, create = Order.objects.get_or_create(customer=customer, complete=False)
		total = float(data['form']['total'])
		order.transaction_id = transaction_id

		if total == order.get_cart_total:
			order.complete = True
		order.save()

		ship= data['shipping']
		if (order.shipping):
			customer_address, create = CustomerAddress.objects.get_or_create(
				customer = customer,
				address=ship['address'],
				kelurahan=ship['kelurahan'],
				kecamatan=ship['kecamatan'],
				kabkot=ship['kabkot'],
				provinsi=ship['provinsi'],
				kode_pos=ship['kode_pos'],)
			shipping = ShippingAddress.objects.create(customer_address=customer_address, order=order)
			Pesanan.objects.create(customer=customer, order=order, shipping=shipping, status="PRO")


	return JsonResponse("Ordered", safe=False)


























