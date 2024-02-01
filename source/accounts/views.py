from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse

from .forms import RegisterUserForm, Profile_user, User_Add
from .models import * 
from shop.models import Calculation_price
from django.views.decorators.csrf import csrf_exempt
from .filters import *
from .decorators import *
import math, json

# imports for email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


# Create your views here.
@unauthenticated_user
def login_user(request):
    try:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("logging in successfull! Hello "+ request.user.get_short_name()))
                return redirect('home')     

            else:
                messages.success(request, ("Username or Password was Incorrect"))
                return redirect('login')
        else:
            return render(request, 'accounts/login.html', {})
    except:
        messages.success(request, ("Internal Server Error"))

    

def logout_user(request):
    logout(request)
    messages.success(request,("You were Loged Out"))
    return redirect('home')

@unauthenticated_user
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                email = form.cleaned_data['email']
                password = form.cleaned_data['password1']
                group = Group.objects.get(name='customers')
                user.groups.add(group)
                user = authenticate(email=email,password=password)
                login(request, user)
                
                customer_modelUpdate = Customer(user_id=request.user.id, State="", address1="", address2="",city="", zip="")
                customer_modelUpdate.save()
                
                messages.success(request, ('Registration Successfull ! Hello '+ request.user.get_short_name()))
                return redirect('home')
            except:
                messages.success(request, ("Server Error !, Registration was unsucessfull"))


    else:
        form = RegisterUserForm()
    return render(request, 'accounts/register_user.html', {
        'form':form,
    })


@allowed_user(allowed_roles=['admin'])
def admin_page(request):
    # try:
    def sendmail(orderId, trackingId, orderEmail):
        html_template = 'tracking_email.html'
        html_msg = render_to_string(html_template, {'order_id': orderId, 'tracking_id':trackingId})
        subject = "Your Stickycat Order #" + orderId + "has been shipped."
        recipient = orderEmail
        email_from = settings.EMAIL_HOST_USER
        message = EmailMessage(subject, html_msg, email_from, recipient)
        message.content_subtype = 'html'
        message.send()
    # except:
    #     messages.success(request, ("Couldn't sent mail"))


    try:
        orders = Order.objects.all().order_by("-date_created")
        customers = CustomUser.objects.all()
        total_orders = orders.count() 
        orders_shipped = orders.filter(order_status='Shipped').count()
    except:
        messages.success(request, ("Couldn't find data in database"))


   


    if request.method == 'POST':
        try:
            tracking_id = request.POST.get('tracking_id')
            order_stat = request.POST.get('order_status')
            order_id = request.POST.get('order_id')
            if order_stat == 'Shipped':
                try:
                    order = Order.objects.get(order_id=order_id)
                    customer = CustomUser.objects.get(id=order.customer_id)
                    email_to = [str(customer.email)]
                    sendmail(order_id,tracking_id,email_to)
                    messages.success(request,"Email Sent")
                except:
                    messages.success(request,"Email not sent")


            cust_order = orders.get(order_id=order_id)
            cust_order.order_trackingId = tracking_id
            cust_order.order_status = order_stat
            cust_order.save()
            messages.success(request, ('Tracking Id and shipping details updated'))
        except:
            messages.success(request, ('Tracking id and status not updated'))

    if request.method == 'GET':
        search = request.GET.get('search')
        if search==None:
            objs = ""
        else:
            objs = Order.objects.filter(order_id__startswith=search)
            
        payload = []

        

        for obj in objs :
            order_obj =  Order.objects.get(order_id=str(obj))
            payload.append(order_obj)

        return render(request, 'accounts/admin_page.html', {'orders':orders,'customers':customers, 'total_orders':total_orders,'Shipped': orders_shipped, 'payload':payload})        

    return render(request, 'accounts/admin_page.html', {'orders':orders,'customers':customers, 'total_orders':total_orders,'Shipped': orders_shipped})

@allowed_user(allowed_roles=['admin'])
def users_page(request, pk_test):
    customer = CustomUser.objects.get(id=pk_test)
    orders = customer.order_set.all()

    total_orders = orders.count()
    orders_shipped = orders.filter(order_status='Shipped').count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders' : orders,
        'total_orders':total_orders,
        'shipped' : orders_shipped,
        'myFilter': myFilter
    }

    
    return render (request, 'accounts/users.html', context)


@csrf_exempt
def del_item(request):
    or_id = request.POST.get('order_id')
    orders = Order.objects.get(order_id=or_id)
    orders.delete()
    return render(request, 'accounts/del_item.html')



def user_profile(request):
    try:
        user_customuserModel = request.user
        user_customerModel = request.user.customer
        profile_form = Profile_user(instance=user_customuserModel)
        add_form = User_Add(instance=user_customerModel) 
        if request.method == "POST":
            profile_form = Profile_user(request.POST, instance=user_customuserModel)
            add_form = User_Add(request.POST, instance=user_customerModel)
            if profile_form.is_valid() and add_form.is_valid():
                profile_form.save()
                add_form.save()
                messages.success(request,"Update Done")
                context = {'form':profile_form, 'address':add_form}
                return render(request, 'accounts/user_profile.html', context)
    except:
        messages.success(request, ("Unknown Server Error"))
        return render(request, 'accounts/user_profile.html')
     

def user_orders(request):
    try:
        customer = CustomUser.objects.get(email=request.user)
        orders = Order.objects.filter(customer_id=customer)
    except:
        messages.success(request, ("Unable to fetch data from servers"))


    context = {
        'orders':orders    
    }
    return render(request, 'accounts/user_orders.html', context)

def invoice(request, order_id):
    try:
        order = Order.objects.get(order_id=order_id)
        cart_items = json.loads(order.order_details)
    except:
        messages.success(request, ("Unable to fetch data from servers, try again later"))
    total_gst = 0
    total_cst = 0
    for key in cart_items:
        price = Calculation_price.objects.get(size=cart_items[key][3])
        cst_cal = math.floor((price.cst_persheet * int(cart_items[key][4]))*1.02)
        qty = price.qty_persheet * int(cart_items[key][4])
        gst = cst_cal*0.18
        total_gst += gst
        total_cst += cst_cal
        cart_items[key].append(qty)
        cart_items[key].append("%.2f" %(cst_cal+gst))
        cart_items[key].append("%.2f" %(gst))
        cart_items[key].append(cst_cal)
    
    if order.order_deliveryState == "Madhya Pradesh":
        tax_type = "CGST/SGST"
    else:
        tax_type = "IGST"
    
    roundoff = total_gst%1
   
    
    context = {
        'order':order,
        'gstSubotal' : ("%.2f" %(total_gst)),
        'roundOff':("%.2f" % roundoff),
        'gstTotal':total_gst-roundoff,

        
        "tax_type" : tax_type,
        "delivery_state" : order.order_deliveryState,
        'cart': cart_items,
        'subTotalCst':("%.2f" %((total_cst*1.18)+70)),
        'totalCst':((total_cst*1.18)+70)-roundoff,

        
    }
    return render(request, 'accounts/invoice.html', context)

def searchapi (request):
  
    search = request.GET.get('search')
    print(f'search is : {search}')
    if search==None:
        objs = ""
    else:
        objs = Order.objects.filter(order_id__startswith=search)
        
    payload = []

    for obj in objs :
        payload.append({
            'order_id' : str(obj)
            
        })

        
    return JsonResponse ({
        'status' : True,
        'payload' : payload
    })
       
