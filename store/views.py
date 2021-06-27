from django.shortcuts import render
import datetime
# Create your views here.
def index(request):
	time = datetime.datetime.now()
	context ={'time': time}
	return render(request,'store/index.html',context)

def store(request):
	return render(request,'store/store.html')

def cart(request):
	return render(request, 'store/cart.html')

def checkout(request):
	return render(request, 'store/checkout.html')
