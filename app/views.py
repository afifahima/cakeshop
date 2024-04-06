from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views import View

from .models import Cart, Customer, Product
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def subject(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'index.html',locals())
@login_required
def about(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"about.html",locals()) 
def contact(request):
    return render(request,"contact.html") 


def Index(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'index.html',locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title= Product.objects.filter(category=val).values('title')

        return render(request,"category.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"category.html",locals())
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"productdetail.html",locals())


class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"customerregistration.html",locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data") 
        return render(request,"customerregistration.html",locals()) 
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,locality=locality, mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congralulation! Profile Save Successfully")
            

        else:
            messages.warning(request,"Invalid Input Data")    

        return render(request,"profile.html",locals())
           


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"address.html",locals())
@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")
@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0 
    for p in cart:
        value = p.quantity * p.product.selling_Price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        

    return render(request,'addtocart.html',locals())   
@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
         user=request.user
         add=Customer.objects.filter(user=user)
         cart_items=Cart.objects.filter(user=user)
         famount = 0
         for p in cart_items:
            value = p.quantity * p.product.selling_Price
            famount = famount + value
            totalamount = famount + 40
            totalitem = 0
         if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            
            return render(request,'checkout.html',locals())
@method_decorator(login_required,name='dispatch')
class Success(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.selling_Price
            famount = famount + value
            totalamount = famount + 40
            totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            return render(request,'success.html',locals())
@login_required
def orders(request):
    totalitem = 0

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    user=request.user
    cart = Cart.objects.filter(user=user)
    return render(request,'orders.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_Price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)    

def minus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.selling_Price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)    



    
@login_required
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect("/cart")
        
    
    



