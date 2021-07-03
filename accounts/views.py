from django.shortcuts import render, redirect
from store.models import *
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, LoginForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
import json
from django.contrib import messages
from django.http import JsonResponse


def loginPage(request):
    form = LoginForm()
    context={}
    if request.user.is_authenticated:
        return redirect("store:store")
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,"You're logged in as " + request.user.username)
                return redirect("store:store")
            else:
                context['form'] = LoginForm()
    else:
        context['form']= LoginForm()
    context['form'] = form
    return render(request, 'accounts/login.html', context)


def register(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("accounts:login")
        else:
            context['form'] = form
    else:
        form = RegistrationForm()
        context['form'] = form
    return render(request, 'accounts/register.html', context)


def logoutPage(request):
    logout(request)
    messages.info(request,"You're logged out")
    return redirect("store:store")


def accounts(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    address = CustomerAddress.objects.filter(
        customer=customer).order_by('-is_default')
    cartItem = order.get_cart_items
    context = {
        'user': customer,
        'cartItem': cartItem,
        'addresses': address
    }
    return render(request, 'accounts/dashboard.html', context)


def addAddress(request):
    data = json.loads(request.body)
    customer = request.user.customer
    new_addr = data['newAddress']
    default = True if new_addr['is_default'] == "True" else False
    print(default)
    if default:
        CustomerAddress.objects.all().update(is_default=False)
    CustomerAddress.objects.create(
        customer=customer,
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
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        cartItem = order.get_cart_items
        context = {
            'cartItem': cartItem,
            'address': address,
            'id': id
        }
        return render(request, 'accounts/edit-address.html', context)
    elif request.method == "POST":
        try:
            default = True if request.POST['is_default'] == "True" else False
            if default:
                CustomerAddress.objects.all().update(is_default=False)
        except:
            default = CustomerAddress.objects.get(id=id).is_default
        CustomerAddress.objects.filter(id=id).update(
            address=request.POST['address'],
            kelurahan=request.POST['kelurahan'],
            kecamatan=request.POST['kecamatan'],
            kabkot=request.POST['kabkot'],
            provinsi=request.POST['provinsi'],
            kode_pos=request.POST['kode_pos'],
            is_default=default
        )
        return redirect('accounts:accounts')

    elif request.method == "PUT":
        CustomerAddress.objects.all().update(is_default=False)
        CustomerAddress.objects.filter(id=id).update(is_default=True)
        return JsonResponse("Address Used", safe=False)
    return render(request, 'accounts/edit-address.html', context)
