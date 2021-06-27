from django.shortcuts import render
from .models import *
import datetime
# Create your views here.
def index(request):
	time = datetime.datetime.now()
	context ={'time': time}
	return render(request,'store/index.html',context)

def store(request):
	product = Product.objects.all()
	context ={
		'products':product
	}
	return render(request,'store/store.html',context)

def cart(request):
	return render(request, 'store/cart.html')

def checkout(request):
	return render(request, 'store/checkout.html')
