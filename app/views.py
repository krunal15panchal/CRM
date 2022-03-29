from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .models import *
from .forms import *
from .filters import *
from .decorators import *

# Create your views here.
@login_required(login_url='login')
@admin_only
def main(request):
    return render(request,'main.html')

@unauthenticated_user
def registerPage(request):
    form=CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
            )
            messages.success(request,'account was created for '+ username)
            return redirect('login/')
    
    context={'form':form}
    return render(request,'register.html',context)
    
@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
             messages.info(request,'Username or Password incorrect')
        
    return render(request,'login.html')



def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count() 
    context={'orders':orders,'total_orders':total_orders,'pending':pending,'delivered':delivered}
    return render(request,'user.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request. POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
                           
           
    context={'form':form}
    return render(request,'accounts_setting.html',context)

@allowed_users(allowed_roles=['admin'])
def dashboard(request):
    orders=Order.objects.all()
    customers=Customer.objects.all()
    total_customers=customers.count()
    total_orders=orders.count()
    delivered=orders.filter(status="Delivered").count()
    pending=orders.filter(status="Pending").count()
    
    params={'orders':orders,'customers':customers,'total_orders':total_orders,
            'delivered':delivered,'pending':pending,}
    return render(request,'dashboard.html',params)

def products(request):
    products=Product.objects.all()
    params={'products':products}
    return render(request,'products.html',params)

def customer(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    orders_count=orders.count()
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs

    context={'customer':customer, 'orders':orders , 'orders_count':orders_count,'myFilter':myFilter}
    
    return render(request,'customer.html',context)

def create_order(request,pk):
    orderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'))
    customer=Customer.objects.get(id=pk)
    #form=OrderForm(initial={'customer':customer})
    formSet=orderFormSet(instance=customer)
    
    if request.method=='POST':
        formSet=orderFormSet(request.POST,instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('/dashboard')
            
    context={'form':formSet}
    return render(request,'order_form.html',context)

def updateOrder(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    
    if request.method=='POST':
         form=OrderForm(request.POST,instance=order)
         if form.is_valid():
            form.save()
            return redirect('/dashboard')
        
    context={'form':form}
    return render(request,'order_form.html',context)

def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/dashboard')
                  
    context = {'item':order}
    return render (request, 'delete.html', context) 
    

