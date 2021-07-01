from django.shortcuts import render, redirect
from store.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def login(request):
	context={}
	return render(request, 'accounts/login.html',context)

def register(request):
	context={}
	return render(request, 'accounts/register.html',context)

def accounts(request):
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	address= CustomerAddress.objects.filter(customer=customer).order_by('-is_default')
	cartItem = order.get_cart_items
	context ={
		'user':customer,
		'cartItem': cartItem,
		'addresses': address
	}
	return render(request,'accounts/dashboard.html',context)

def addAddress(request):
	data = json.loads(request.body)
	customer = request.user.customer
	new_addr = data['newAddress']
	default = True if new_addr['is_default']=="True" else False
	if default:
		CustomerAddress.objects.all().update(is_default=False)
	CustomerAddress.objects.create(
		customer = customer,
		address=new_addr['address'],
		kelurahan=new_addr['kelurahan'],
		kecamatan=new_addr['kecamatan'],
		kabkot=new_addr['kabkot'],
		provinsi=new_addr['provinsi'],
		kode_pos=new_addr['kode_pos'],
		is_default=new_addr['is_default']
		)
	return JsonResponse("Address added", safe=False)

def deleteAddress(request, id):
	CustomerAddress.objects.get(id=id).delete()
	return JsonResponse("Address deleted", safe=False)


def editAddress(request, id):
	if request.method == "GET":
		address = CustomerAddress.objects.get(id=id)
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		cartItem = order.get_cart_items
		context ={
			'cartItem': cartItem,
			'address': address,
			'id':id
		}
		return render(request, 'accounts/edit-address.html', context)
	elif request.method=="POST":
		print(request.POST)
		if request.POST['is_default'] == "True":
			CustomerAddress.objects.all().update(is_default=False)
		CustomerAddress.objects.filter(id=id).update(
			address=request.POST['address'],
			kelurahan=request.POST['kelurahan'],
			kecamatan=request.POST['kecamatan'],
			kabkot=request.POST['kabkot'],
			provinsi=request.POST['provinsi'],
			kode_pos=request.POST['kode_pos'],
			is_default=True if request.POST['is_default'] == "True" else False
			)
		return redirect('accounts:accounts')

	elif request.method=="PUT":
		CustomerAddress.objects.all().update(is_default=False)
		CustomerAddress.objects.filter(id=id).update(is_default=True)
		return JsonResponse("Address Used", safe=False)
	return render(request, 'accounts/edit-address.html', context)